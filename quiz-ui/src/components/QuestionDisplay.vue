
<template>
</template>

<script>
export default {
  props: {
    question: {
      type: Object
    }
  },
  created() {
    // props are exposed on `this`
    console.log(this.question)
  }
}
</script>
