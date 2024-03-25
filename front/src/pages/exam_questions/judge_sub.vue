<template>
    <div>
        <p><strong>提示：本页面判多少，返回顶部点击“提交判分结果”按钮提交，未判分的学生答案不受影响，重新回到本页面可以刷新出未判分的学生答案。</strong><br></p>
        <el-affix :offset="150">
            <!-- <el-col :span="12"> -->
                <!-- <div class="fixed-button"> -->
                <!-- <div> -->
                <el-button @click="submitCount" type="primary">提交判分题目</el-button>
                <!-- </div> -->
            <!-- </el-col> -->
        </el-affix>
        <br>
        <el-col :span="12">
            <div v-for="(question, index) in questions" :key="index">
                <!-- 题号 + 题目 -->
                <p>{{ index + 1 }}. 【{{ question.question_type }}】 {{ question.exam_question }}</p>

                <p><strong>参考答案：</strong><br>
                <div class="answer-box">
                    <pre> {{ question.reference_answer }} </pre>
                </div>
                </p>

                <p><strong>学生答案：</strong><br>
                <div class="answer-box">
                    <pre> {{ question.stu_answer }}</pre>
                </div>
                </p>

                <!-- 判分 -->
                <el-radio-group v-model="question.score" class="large-radio">
                    <el-radio v-for="option in scoreOptions(question.set_score)" :value="option">{{ option }}</el-radio>
                </el-radio-group>
            </div>

        </el-col>
    </div>
</template>
  
<script>
import { toast } from "~/composables/util"
import { ElMessageBox } from 'element-plus';
import { get_sub_without_score, submit_sub_score } from "~/api/judge"
import { useRouter } from 'vue-router';

export default {
    name: "examing",
    data() {
        return {
            questions: [],
            examId: null,
            tableData: null
        };
    },

    // computed: {

    // },

    created() {
        this.examId = this.$router.currentRoute.value.query.examId;
        if (!this.examId) {
            this.examId = 0
        }

        get_sub_without_score(this.examId)
            .then(res => {
                this.questions = res.data;
            })
    },
    updated() {
        console.log(this.questions);
    },
    methods: {

        scoreOptions(set_score) {
            const maxScore = parseFloat(set_score); // 将字符串解析为数字
            return Array.from({ length: maxScore + 1 }, (_, index) => index); // 生成从1到最大分数的数组
        },

        submitCount() {
            submit_sub_score(this.questions);
            alert('提交成功!');

            // 重新刷新剩余题目
            location.reload();
        }
    }
};
</script>
<style scoped>
.answer-box {
    border: 1px solid #ccc;
    padding: 10px;
    margin-bottom: 10px;
}

.large-radio {
    font-size: 40px;
    /* 改变单选按钮的字体大小 */
}

.large-radio .el-radio-button {
    height: 80px;
    /* 改变单选按钮的高度 */
    line-height: 80px;
    /* 改变单选按钮的行高 */
}

.large-radio .el-radio-button .el-radio-button__inner {
    font-size: 16px;
    /* 改变单选按钮标签的字体大小 */
}

.large-radio-option {
    margin-right: 30px;
    /* 增加单选按钮之间的间距 */
}

.fixed-button {
    position: fixed;
    /* 固定定位 */
    top: 50px;
    /* 距离顶部的距离 */
    right: 20px;
    /* 距离右侧的距离 */
}

</style>