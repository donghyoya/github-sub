<script>
import 'highlight.js/lib/common';
import hljsVuePlugin from "@highlightjs/vue-plugin";

export default{
    props: {
        src: String,
        language: String
    }
}
</script>

<template>
<highlightjs
        :language="language"
        :code="src"
    />
</template>

<style scoped>
*{
    font-size: 0.5em;
}
</style>