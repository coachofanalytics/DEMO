<template>
  <div class="about">
    <h1>{{ title }}</h1>
    <p>{{ description }}</p>
  </div>
  <Members/>
</template>

<script>
// We import components and Views
import Members from '@/components/Members.vue';

// Write methods and compute functions
export default {
name: 'Team',
components: {
  Members
},
data() {
  return{
        title:'About US',
        header:'This',
        description:'This is an about page',
    }
},
}
</script>

