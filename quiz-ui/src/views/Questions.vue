<style>
</style>


<template>
  <h1>Questions</h1>
</template>

<script>
import participationStorageService from "../services/ParticipationStorageService";

export default {
  name: "Questions",
  data() {
    return {
    };
  },
  methods: {

  },
  async created() {
    console.log(this.username);
  }

};
</script>