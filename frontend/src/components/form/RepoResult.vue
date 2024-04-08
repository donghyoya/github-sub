<script setup>
import SourceContent from './SourceContent.vue';
const props = defineProps({
    srcObject: Object
});
</script>

<template>

<li>
    <details>
        <summary>
            <a :href="srcObject.url" target="_blank">
                {{ srcObject.directory }}
            </a>
            <p>
                {{ srcObject.title }}
            </p>
        </summary>
        <SourceContent :src="srcObject.src" :language="srcObject.language" />
    </details>
</li>

</template>

<style scoped>
li{
    width: 100%;
    margin: 0;
    padding: 0;
}
summary {
    display: list-item; 
    list-style: none; 
    cursor: pointer; 
    padding: 5px; 
    background-color: #f0f0f0; 
    border: 1px solid #ccc; 
    border-radius: 5px; 
}

details[open]{
    margin: 10px 0;
}

details[open] summary {
    background-color: #e0e0e0; 
    border-radius: 5px 5px 0 0;
}

details[open] div{
    border: 1px solid #ccc; 
    padding: 10px;
    font-size: 0.7em; 
    border-radius: 0 0 5px 5px;
}

summary::marker {
    color: #333; 
    font-weight: bold; 
}

summary::-webkit-details-marker {
    color: #333; 
}

</style>