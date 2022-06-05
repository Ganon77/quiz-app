<style>
@import './assets/css/base.css';
@import './assets/css/navbar.css';
</style>

<script setup>
import { RouterLink, RouterView } from 'vue-router'
</script>

<template>
  <header>
    <div class="wrapper">
      <nav>

        <RouterLink to="/" class="navlink">
          <div class="linkContent">
            Home
          </div>
        </RouterLink>

        <RouterLink to="/admin" class="navlink">
          <div class="linkContent">
            Admin
          </div>
        </RouterLink>
      </nav>
    </div>
  </header>

  <RouterView />
</template>
