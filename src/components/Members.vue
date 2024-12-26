<template>
      <h1>Our Team</h1>
      <p>{{ description }}</p>
    <div v-for = "member in members" :key="member.id" class="TeamMember">
      <!-- <span @click="deleteMember(member)">{{member}}</span> -->
      <!-- <router-link :to="{ name: 'MemberDetails', params: { id: member.id }}">
        <h2>{{ member.id }}</h2>
        <h2>{{ member.name }}</h2>
        <h2>{{ member.title }}</h2>
      </router-link> -->
      <h2>{{ member.id }}</h2>
      <h2>{{ member.name }}</h2>
      <h2>{{ member.title }}</h2>
    </div>
  </template>


<script>
export default {
  name: 'Members',
  props:['header','description','theme'],

  data() {
      return {
        members: [
          {name:'Chris Maghas', title: 'Project Manager', id: 1, details: 'lorem',tenure:0},
          {name:'Nane Doe', title: 'UX Designer', id: 2, details: 'lorem',tenure:0 },
          {name:'Sera Angie',title:'Web Developer', id: 3, details: 'lorem',tenure:0 },
          {name:'Luke Bonnie', title: 'Vue Developer', id: 4, details: 'lorem',tenure:0 }
        ],
        description:"The Board Members of CODA comprise a distinguished group of leaders with a broad spectrum of expertise in the IT industry and business management.",
      };
    },

    methods : {
    deleteMember() {
    //   this.members = this.members.filter((item) => {
    //   return members !== item;
    // });
    console.log('Member Deleted')
    }
  }
}
</script>

<style>

.TeamMember {
  display: inline-block;
  margin: 20px 10px 0 0;
  padding: 6px 12px;
  background: #eee;
  border-radius: 20px;
  font-size: 12px;
  letter-spacing: 1px;
  font-weight: bold;
  color: #777;
  cursor:pointer;
}
</style>