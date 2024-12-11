<script setup lang="ts">
</script>
<template>
    <div style="width: 1080px;margin: 0 auto;">
    <h1 style="text-align: center;">面向科学发现的Research Agent</h1>
    <p>&nbsp;</p>
    <p>在以 LLM 为驱动的 AI Agents 系统中，LLM 是代理系统的“大脑”，并需要其他几个关键组件的辅助：</p>
    <p style="font-size: 1.5em;">1. 规划（Planning）</p>
    <ul>
        <li><span class="liB">子目标和分解：</span>AI Agents 能够将大型任务分解为较小的、可管理的子目标，以便高效的处理复杂任务；</li>
        <li><span class="liB">反思和细化：</span>Agents 可以对过去的行为进行自我批评和反省，从错误中吸取经验教训，并为接下来的行动进行分析、总结和提炼，这种反思和细化可以帮助 Agents 提高自身的智能和适应性，从而提高最终结果的质量。</li>
    </ul>
    <p style="font-size: 1.5em;">2. 记忆 （Memory）</p>
    <ul>
        <li><span class="liB">短期记忆：</span>所有上下文学习都是依赖模型的短期记忆能力进行的；</li>
        <li><span class="liB">长期记忆：</span>这种设计使得 AI Agents 能够长期保存和调用无限信息的能力，一般通过外部载体存储和快速检索来实现。</li>
    </ul>
    <p style="font-size: 1.5em;">3. 工具使用（Tool use）</p>
    <ul>
        <li>AI Agents 可以学习如何调用外部 API，以获取模型权重中缺少的额外信息，这些信息通常在预训练后很难更改，包括当前信息、代码执行能力、对专有信息源的访问等。</li>
        
    </ul>
    <img src="/img/agent.png" alt="">
    <p style="font-size: 1.3em;text-align: center;">【coming soon】</p>
</div>
</template>
<style scoped>
h1 {
    font-size: 2em;
}

.liB {
    font-weight: bold;
}
* {
    line-height: 2;
}
</style>