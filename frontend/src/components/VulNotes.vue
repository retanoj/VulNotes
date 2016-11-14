<template>
  <div class="vul-notes">
    <div class="container">
      <headline></headline>
      <list-component></list-component>
    </div>
  </div>
</template>

<script>
import headline from './Headline'
import listComponent from './List'

export default {
  components: {
    headline,
    'list-component': listComponent
  }
}
</script>

