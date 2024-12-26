<template>
  <div class="about">
    <h1>{{ title }}</h1>
    <p>{{ description }}</p>
  </div>
  <div>
    <Members/>
  </div>
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
        header:'This is an about page',
        description:'This is an about page',
    }
},
}
</script>

