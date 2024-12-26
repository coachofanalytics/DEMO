<template>
    <div>
            <h1>Member Details Page</h1>
            <div v-if="member">
                <p>Name: {{ member.name }}</p>
                <p>Member ID: {{ member.id }}</p>
                <p>Title: {{ member.title }}</p>
            </div>
            <div v-else>
                <p>The Members loading......</p>
            </div>
            <button @click="deleteMember(Number(id))">Delete Member</button>
    </div>
  </template>

  <script>
    import Members from './Members.vue';
  export default {
    props: ['id'],
    data() {
            return {
                member: null,
                // memberid : null
            };
        },
        methods: {
            // deleteMember(memberId) {
            // this.Members = this.Members.filter((item) => {
            //     return item.id !== memberId;
            // });
            // }== memberId;
            // });
            deleteMember(id) {
                // Number(id)
                // memberid=this.id
                console.log(id)
            }
        },
    mounted() {
        fetch('http://localhost:3000/members/' + this.id)
            // ✅ Call res.json() as a method
            .then(res => res.json())
            // ✅ Update the members array 
            .then(data => this.member = data) 
            // ✅ Log error messages
            .catch(err => console.log('Fetch error:', err.message)); 
        },
  }
  </script>
  
  <style>
  </style>
  