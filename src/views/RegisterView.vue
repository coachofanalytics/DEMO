<template>
    <div v-if="showModal">
        <SignUp :header="header" :description="description" :theme="SignUp"/>
    </div>
    <button @click="toggleModal">{{title}}</button>
</template>

<script>
// We import components and Views
import SignUp from '@/components/SignUp.vue';

// Write methods and compute functions
export default {
  name: 'RegisterView',
  components: {
    SignUp
  },
  data() {
    return{
        title:'Sign UP',
        header:'Welcome to CODA, Are you NEW here?',
        description:'Sign-up to enjoy all the benefits and trainings CODA provides.',
        showModal:false
    }
  },

  methods: {
    toggleModal() {
      this.showModal = !this.showModal
    },
  }

}
</script>


<style>


</style>