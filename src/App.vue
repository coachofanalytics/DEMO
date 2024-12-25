<template>
  <img alt="coda logo" src="./assets/coda_logo.jpg">
  <h1>{{title}}</h1>
  <div v-if="showModal">
    <SignUp :header="header" :text="text" :theme="SignUp"/>
  </div>
  <div v-if="showModal">
    <ModalComponent :header="header" :text="text" :theme="sale" @close="toggleModal"/>
  </div>
  <button @click="toggleModal">Sign Up</button>
  <button @click="toggleWorld">Open Greetings</button>
</template>

<script>
import SignUp from './components/SignUp.vue'
import ModalComponent from './components/ModalComponent.vue'

export default {
  name: 'App',
  components: {
    SignUp,
    ModalComponent,
  },
  data() {
    return{
      title:'CODA APP',
      header:'Sign Up for our classes!',
      text: 'On a scale of 0-10 enter your level of understanding for technical roles',
      showModal: true,
      showgreetings: false
    }
  },
  methods : {
    toggleModal() {
      this.showModal = !this.showModal
    },
    toggleWorld() {
      this.showgreetings = !this.showgreetings
    },
  },
  // methods : {
  //   toggleModal() {
  //     this.showModal = !this.showModal
  //   }
  // }
}

</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
