<template>
    <h1>{{ header }}</h1>
    <h3>Basic Information</h3>
  
    <form @submit.prevent="handleSubmit">
      <label>Email</label>
      <input type="email" required v-model="email">
      <label>Password</label>
      <input type="password" required v-model="password">
      <div v-if="passwordError" class="error">
        {{passwordError}}
      </div>
     
      <p>Select your highest educational level?*</p>
      <select v-model="education">
        <option value="degree">Degree</option>
        <option value="college">Some College</option>
        <option value="college">High School</option>
      </select>
      <div>
        <input type="checkbox" required v-model="terms">
        <label>Terms and Conditions</label>
      </div>
      <h3>Skill Set</h3>
      <input type="text"  v-model="tempskill" @keyup="addskill">
      <div v-for = "skill in skills" :key="skill" class="pill">
        <span @click="deleteSkill(skill)">{{skill}}</span>
      </div>
      <p>{{ text }}</p>
    <h3>Experience</h3>
      <p>Please Check the Tools You are Familiar with</p>
      <div>
        <input type="checkbox" value="tableau" v-model="courses">
        <label>Tableau</label>
      </div>
      <div>
        <input type="checkbox" value="alteryx" v-model="courses">
        <label>Alteryx</label>
      </div>
      <div>
        <input type="checkbox" value="python" v-model="courses">
        <label>Python</label>
      </div>

      <div class="submit">
        <button>Submit Information</button>
      </div>
    </form>
    <p>Email: {{ email }}</p>
    <p>Password: {{ password }}</p>
    <p>education: {{ education }}</p>
    <p>terms: {{ terms }}</p>
    <p>courses: {{ courses }}</p>
</template>

<script>
export default {
  name: 'SignUp',
  props:['header','text','theme'],

  data(){
    return{
      email:'',
      password:'',
      education:'',
      terms:false,
      courses:[],
      tempskill:'',
      skills:[],
      passwordError:'',
      errorMessage:'Password Must be more than 6 characters in length'

    }
  },
  methods: {
    addskill(e) {
      if (e.key === ',' && this.tempskill){
        if (!this.skills.includes(this.tempskill)){
          this.skills.push(this.tempskill)
        }
        this.tempskill=''
      }
        // console.log(e)
    },
    deleteSkill(skill) {
    this.skills = this.skills.filter((item) => {
        return skill !== item;
    });
    },
    handleSubmit() {
      this.passwordError=this.password.length > 5 ? "" : this.errorMessage
      if (!this.passwordError){
        console.log("email",this.email)
        console.log("password",this.password)
        console.log("education",this.education)
        console.log("courses",this.courses)
        console.log("skills",this.skills)
      }

    }
  }

}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
form {
    max-width: 420px;
    margin: 30px auto;
    background: white;
    text-align: left;
    padding: 40px;
    border-radius: 10px;
  }
label {
  color: #aaa;
  display: inline-block;
  margin: 25px 0 15px;
  font-size: 0.6em;
  text-transform: uppercase;
  letter-spacing: 1px;
  font-weight: bold;
}

input {
  display: block;
  padding: 10px 6px;
  width: 100%;
  box-sizing: border-box;
  border: none;
  border-bottom: 1px solid #ddd;
  color: #555;
}


input[type="checkbox"] {
    display: inline-block;
    width: 16px;
    margin: 0 10px 0 0;
    position: relative;
    top: 2px;
  }

  .pill {
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

button {
    background: #0b6dff;
    border: 0;
    padding: 10px 20px;
    margin-top: 20px;
    color: white;
    border-radius: 20px;
}

.submit {
    text-align: center;
}
</style>
