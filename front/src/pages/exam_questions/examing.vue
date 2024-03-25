<template>
  <div v-if="examId">

    <el-affix :offset="126" >
      <!-- <div class="flex gap-2"> -->
      <el-tag type="primary" v-if="remainingTime + 1 > 3">剩余时间：{{ remainingTime + 1 }} 分钟</el-tag>
      <el-tag type="warning" v-else>剩余时间：{{ remainingTime + 1 }} 分钟</el-tag>
      <!-- </div> -->
    </el-affix>

    <div v-if="!tableData || !tableData.length">
      <el-col :span="12">
        <div class="grid-content bg-purple">
          <el-tag type="error" v-if="multiple_half">多选题少选得一半分</el-tag>
          <el-tag type="error" v-else>多选题少选不得分</el-tag>
          <div v-for="(question, index) in questions" :key="index">
            <!-- 题号 + 题目 -->
            <p>{{ index + 1 }}. 【{{ question.question_type }}】 {{ question.question_text }}</p>

            <!-- 单选题 -->
            <el-radio-group v-if="question.question_type == '单选'" v-model="question.stu_answer">
              <el-radio v-for="(option, index) in question.options" :value="option" :key="option">{{ option }}</el-radio>
            </el-radio-group>

            <!-- 多选题 -->
            <el-checkbox-group v-else-if="question.question_type == '多选'" v-model="question.stu_answer">
              <!-- label绑定答案的值,可以绑定索引index,也可以绑定答案内容city -->
              <el-checkbox v-for="(option, index) in question.options" :value="option">{{ option
              }}</el-checkbox>
            </el-checkbox-group>

            <!-- 判断题 -->
            <el-radio-group v-if="question.question_type == '判断'" v-model="question.stu_answer">
              <el-radio value="正确">正确</el-radio>
              <el-radio value="错误">错误</el-radio>
            </el-radio-group>


            <!-- 填空题 -->
            <el-radio-group v-if="question.question_type == '填空'" v-model="question.stu_answer">
              <el-input type="textarea" :rows="2" placeholder="请输入内容" v-model="question.stu_answer"></el-input>
            </el-radio-group>


            <!-- 简答题 -->
            <div v-if="question.question_type == '简答'">
              <el-input type="textarea" :rows="3" placeholder="请输入内容" v-model="question.stu_answer"></el-input>
            </div>

            <!-- 论述题 -->
            <div v-if="question.question_type == '论述'">
              <el-input type="textarea" :rows="6" placeholder="请输入内容" v-model="question.stu_answer"></el-input>
            </div>

          </div>
        </div>
        <br />
      </el-col>

      <el-col :span="12">
        <div>
          <el-button @click="submitCount('manual submit')" type="primary">提交考卷</el-button>
        </div>
      </el-col>
    </div>
    <!-- 分割线， 上为考试，下为错题复现 -->
    <div v-if="tableData && tableData.length">
      <!-- <el-col :span="12">
      <div class="grid-content bg-purple">
        <div v-for="(question, index) in tableData" :key="index">

        </div>
      </div>
      <br />
    </el-col> -->
      <el-row>
        <el-col :span="24">
          <div class="grid-content bg-purple">
            <div v-for="(question, index) in tableData" :key="index" class="question">
              <div class="answer-box">
                <p><strong>问题：</strong> {{ question.exam_question }}</p>
                <p><strong>学生答案：</strong>
                <div class="answer-box">
                  <pre>{{ question.stu_answer }}</pre>
                </div>
                </p>
                <p><strong>参考答案：</strong>
                <div class="answer-box">
                  <pre>{{ question.choice_text }}</pre>
                </div>
                <div class="answer-box">
                  <pre>{{ question.reference_answer }}</pre>
                </div>
                </p>
                <p><strong>得分：</strong>{{ question.score }}</p>
              </div>
            </div>
          </div>
          <br><br><br>
        </el-col>
      </el-row>
    </div>
  </div>
  <div v-else>
    <p>从<strong>考试列表</strong>进入考试</p>
  </div>
</template>

<script>
import { toast } from "~/composables/util"
import { ElMessage, ElMessageBox } from 'element-plus'
import {
  exam_manage_get,
  get_exam_paper, submit_exam_paper, detect_examed, get_old_results, check_idcard_tail
} from "~/api/examing"
import { useRouter } from 'vue-router';
import { onBeforeUnmount, onMounted, ref } from 'vue';
import { useStore } from 'vuex'

export default {
  name: "examing",
  data() {
    return {
      questions: [],
      examId: null,
      tableData: null,

      MouseOutCount: 0,
      FullscreenChangeCount: 0,
      VisibilityChangeCount: 0,


      isFullScreen: false,
      isPageActive: true,

      remainingTime: 0, // 剩余时间，单位：分钟
      timer: null, // 定时器
      start_time: null,
      end_time: null,
    };
  },

  setup() {
    const store = useStore();
    return { store };
  },

  watch: {
    MouseOutCount(newValue, oldValue) {
      console.log('MouseOutCount 变化了:', newValue);
      console.log('cheat_mouse_out:', this.store.state.settings.cheat_mouse_out);
      if (newValue >= this.store.state.settings.cheat_mouse_out) {
        console.log('MouseOutCount 已达到阈值，触发特定动作');
        this.submitCount("cheat submit");
      }
    },
    FullscreenChangeCount(newValue, oldValue) {
      console.log('FullscreenChangeCount 变化了:', newValue);
      if (newValue >= 1) {
        console.log('FullscreenChangeCount 已达到阈值，触发特定动作');
        this.submitCount("cheat submit");
      }
    },
    VisibilityChangeCount(newValue, oldValue) {
      console.log('VisibilityChangeCount:', this.store.state.settings.cheat_page_out);
      console.log('VisibilityChangeCount 变化了:', newValue);
      if (newValue >= this.store.state.settings.cheat_page_out) {
        console.log('VisibilityChangeCount 已达到阈值，触发特定动作');
        this.submitCount("cheat submit");
      }
    },
  },

  created() {
    const router = useRouter(); // 定义 router 常量
    // 获取 examId
    this.examId = router.currentRoute.value.query.examId;
    console.log('examId:', this.examId);

    exam_manage_get(this.examId).then(res => {
      this.start_time = res.start_time;
      this.end_time = res.end_time;
      this.exam_type = res.exam_type;
      this.exam_name = res.exam_name;
      this.multiple_half = res.multiple_half;
      console.log('考试开始时间:', this.start_time);
      console.log('考试结束时间:', this.end_time);
      console.log('考试名称:', this.exam_name);
      console.log('考试类型:', this.exam_type);
      console.log('多选半分策略:', this.multiple_half);
    }).then(() => {


      // 未到开考时间禁止参加考试
      console.log('开始时间判定：给targetTime传参的end_time:', this.start_time);
      const targetStartTime = new Date(this.start_time).getTime();
      const currentTime_JudgeStartTime = new Date().getTime();
      const timeDiff_JudgeStartTime = currentTime_JudgeStartTime - targetStartTime;
      if (timeDiff_JudgeStartTime < 0) {
        alert("未到开考时间，禁止参加考试");
        this.$router.push({ name: "/exam/list" });
      }

      // 判断是否参加过本次考试
      detect_examed(this.examId)
        .then(res => {
          if (res.double_check == true) {
            if (res.exam_type == "考试") {
              ElMessageBox.alert('请勿重复参加', res.exam_type, {
                confirmButtonText: '确定',
                type: 'warning',
                callback: () => {
                  this.$router.push({ name: "/exam/list" });
                }
              });
            } else {
              // 参加过本次测试，但是本次测试不是考试
              get_old_results(this.examId).then(res => {
                this.tableData = res.data;
              })
            }
          } else {
            console.log('未参加过');
            this.startCountdown();

            // 考试反作弊告警
            ElMessageBox.alert('已开始监听鼠标和切屏事件，勿将鼠标移动页面之外、勿切屏，否则导致提前交卷。', '防作弊警示', {
              confirmButtonText: '确定',
              type: 'warning',
              callback: () => {
                console.log('用户点击了确定按钮');
              }
            });

            ElMessageBox.alert('不要刷新页面，否则答卷数据丢失。', '警示', {
              confirmButtonText: '确定',
              type: 'warning',
              callback: () => {
              }
            });

            ElMessageBox.alert('即将全屏进入考试。', '考试提示', {
              confirmButtonText: '确定',
              type: 'warning',
              callback: () => {
                // 启动全屏
                console.log('开全屏');
                document.documentElement.requestFullscreen();
              }
            });

            // 鼠标监控、切屏监控
            // 【考试监控模块】  -- Start --
            // 无法通过 JavaScript 强制用户全屏并阻止使用键盘快捷键切出屏幕的。浏览器限制了这样的行为，以确保用户对自己的设备有控制权，防止滥用和滋扰。
            // 监控页面是否活动

            console.log('考试开始，设置监听器');
            // 启动全屏
            // document.documentElement.requestFullscreen();
            // 监听全屏事件，检查用户是否自己Esc切出屏幕
            document.addEventListener('fullscreenchange', this.handleFullscreenChange);
            // 监听鼠标离开页面事件
            window.addEventListener('mouseout', this.handleMouseOut);
            // 监听页面是否活动，检测用户是否最小化或后台
            document.addEventListener('visibilitychange', this.handleVisibilityChange);
            // 禁止右键
            window.addEventListener('contextmenu', (event) => {
              event.preventDefault();
            });


            // 获取试卷
            get_exam_paper(this.examId).then(res => {
              // 对选项进行切割
              this.questions = res.question_list.map(question => {
                if (question.question_type === '多选' || question.question_type === '单选') {
                  question.options = question.choice_text.split('|').map(option => option.trim());
                }
                // question.options = question.choice_text.split('|').map(option => option.trim());
                return question;
              });
            })

          }
        })
    })

  },
  updated() {
    console.log(this.questions);
  },
  methods: {
    // 倒计时
    startCountdown() {
      // const targetTime = parse(this.end_time, 'yyyy-MM-dd HH:mm:ss', new Date()).getTime();
      console.log('结束时间判定：给targetTime传参的end_time:', this.end_time);
      const targetTime = new Date(this.end_time).getTime();
      const currentTime = new Date().getTime();
      const timeDiff = (targetTime - currentTime) / (1000);
      // console.log('targetTime:', targetTime);
      // console.log('currentTime:', currentTime);
      // console.log('timeDiff:', timeDiff);

      // 如果剩余时间大于 0，则设置定时器
      if (timeDiff > 0) {
        this.remainingTime = Math.floor(timeDiff / (60)); // 将毫秒转换为分钟
        console.log('剩余时间（分钟）:', this.remainingTime);
        this.timer = setTimeout(() => {
          this.startCountdown(); // 递归调用 startCountdown()，实现持续的倒计时
        }, 1000); // 每隔 1 秒触发一次定时器
      } else {
        console.error('目标时间已过，自动交卷', timeDiff / (1000 * 60));
        this.submitCount("timeout submit");
      }
    },

    // 监控鼠标是否移出
    handleMouseOut(event) {
      if (!event.relatedTarget || event.relatedTarget.nodeName === 'HTML') {
        console.log('鼠标移出页面');
        this.MouseOutCount++;
        toast("鼠标移出次数: " + this.MouseOutCount, "warning");
      }
    },
    // 监控全屏事件
    handleFullscreenChange() {
      // 全屏后隐藏Aside， 同时也避免因Aside导致“鼠标移出页面”的误判（鼠标移动到Aside会导致误判）
      this.isFullScreen = !!document.fullscreenElement;

      if (!this.isFullScreen) {
        console.log('用户退出全屏');
        this.FullscreenChangeCount++;
        toast("退出全屏次数: " + this.FullscreenChangeCount, "warning");

        this.store.dispatch("setExamMode", false)
      } else {
        console.log('用户进入全屏');
        this.store.dispatch("setExamMode", true);
      }
    },
    // 监听页面是否是活动页面
    handleVisibilityChange() {
      this.isPageActive = document.visibilityState === 'visible';
      if (this.isPageActive) {
        console.log('页面在前台活动');
      } else {
        console.log('页面在后台或最小化');
        this.VisibilityChangeCount++;
        toast("切屏次数: " + this.VisibilityChangeCount, "warning");
      }
    },

    submitCount(check) {
      if (check == "manual submit") {
        // 是否答完
        let isComplete = true;
        this.questions.forEach((question, i) => {
          if (!question.stu_answer || question.stu_answer.length === 0) {
            isComplete = false;
            return;
          }
        })

        if (isComplete) {
          // 要求用户输入身份证后六位才提交试卷

          ElMessageBox.prompt('输入身份证后六位', '交卷验证', {
            confirmButtonText: 'OK',
            cancelButtonText: 'Cancel',
          })
            .then(({ value }) => {
              // 交卷验证身份证后六位
              check_idcard_tail(value)
                .then(res => {
                  if (res.data == true) {
                    // 提交试卷
                    submit_exam_paper(this.examId, this.questions)
                      .then(res => {
                        alert('交卷成功!', value);

                        // 考试结束，移除监听
                        console.log('考试结束，移除监听');
                        // 退出全屏
                        document.exitFullscreen();
                        window.removeEventListener('mouseout', this.handleMouseOut);
                        document.removeEventListener('fullscreenchange', this.handleFullscreenChange);
                        document.removeEventListener('visibilitychange', this.handleVisibilityChange);
                        this.$router.push({ name: "/exam/list" });
                      })
                  } else {
                    ElMessage({
                      type: 'info',
                      message: '验证失败',
                    })
                  }
                })
            })

        } else {
          ElMessageBox.alert('', '题目未答完', {
            confirmButtonText: '确定',
            type: 'warning',
            callback: () => {
            }
          });
        }
      } else if (check == "cheat submit") {
        // 用户触发作弊，自动强制交卷
        // 提交试卷
        console.log(this.examId);
        console.log(this.questions);
        // alert后，点击 “确定” 或者 ESC 退出弹窗，都会自动交卷submit_exam_paper()
        alert('由于触发作弊机制，已自动交卷!未答题目不进行任何统计！');
        submit_exam_paper(this.examId, this.questions)
          .then(res => {


            // 考试结束，移除监听
            console.log('考试结束，移除监听');
            // 退出全屏
            document.exitFullscreen();

          })
          .catch(err => {
            console.log(err);
          })
        window.removeEventListener('mouseout', this.handleMouseOut);
        document.removeEventListener('fullscreenchange', this.handleFullscreenChange);
        document.removeEventListener('visibilitychange', this.handleVisibilityChange);
        this.$router.push({ name: "/exam/list" });

      } else if (check == "timeout submit") {

        console.log('时间到，自动交卷');
        // 用户触发作弊，自动强制交卷
        // 提交试卷
        console.log(this.examId);
        console.log(this.questions);
        // alert后，点击 “确定” 或者 ESC 退出弹窗，都会自动交卷submit_exam_paper()
        alert('时间到，已自动交卷!');
        submit_exam_paper(this.examId, this.questions)
          .then(res => {
            // 考试结束，移除监听
            console.log('考试结束，移除监听');
            // 退出全屏
            document.exitFullscreen();
          })
          .catch(err => {
            console.log(err);
          })
        window.removeEventListener('mouseout', this.handleMouseOut);
        document.removeEventListener('fullscreenchange', this.handleFullscreenChange);
        document.removeEventListener('visibilitychange', this.handleVisibilityChange);
        this.$router.push({ name: "/exam/list" });
      }
    }
  }
};
</script>
<style>
.answer-box {
  border: 1px solid #ccc;
  padding: 10px;
  margin-bottom: 10px;
}
</style>