<template>
    <div class="about">
      <h1>Our Team</h1>
      <p>{{ description }}</p>
    </div>
    <div v-for = "member in members" :key="member" class="TeamMember">
      <span @click="deleteMember(member)">{{member}}</span>
    </div>
  </template>
  
<script>
export default {
  name: 'Members',
  props:['header','description','theme'],
  
  data() {
    return{
        first_name:'',
        last_name:'',
        tenure:0,
        description:"The Board Members of CODA comprise a distinguished group of leaders with a broad spectrum of expertise in the IT industry and business management.",
        members:['Chris','James','Nick'],
        
      }
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