<template>
    <div class="backdrop" @click="closeModal">
        <div class="modal" :class="{sale: theme==='sale'}">
            <!-- <h1>{{ header }}</h1>
            <p>{{ text }}</p> -->
        </div>
    </div>
</template>

<script>
    export default{
        // props:['header','text','theme'],
        methods : {
            closeModal() {
            this.$emit('close')
            }
        }
    }
</script>

<style>
.modal {
    width:400px;
    padding:20px;
    margin:100px auto;
}
.modal h1 {
    color:rgb(5, 19, 31);
    /* border:none; */
    padding:0;

 }
 .modal p {
    font-style: normal;
 }
.modal.sale {
    background:crimson;
    color:white
}
</style>