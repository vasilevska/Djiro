<template>
<div>
  <b-navbar toggleable="lg" type="light" variant="light">
    <b-navbar-brand href="#">Điro</b-navbar-brand>

    <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>

    <b-collapse id="nav-collapse" is-nav>
      <!-- Right aligned nav items -->
      <b-navbar-nav class="ml-auto">
         <b-navbar-nav>
          <b-nav-item href="#">Postani Điler</b-nav-item>
      </b-navbar-nav>
        <b-nav-item-dropdown right>
          <!-- Using 'button-content' slot -->
          <template #button-content>
            <em>Korisnik</em>
          </template>
          <b-dropdown-item href="#">Profile</b-dropdown-item>
          <b-dropdown-item href="#">Sign Out</b-dropdown-item>
        </b-nav-item-dropdown>
      </b-navbar-nav>
    </b-collapse>
  </b-navbar>
</div>
</template>


<script>


export default defineComponent({
    setup() {
        
    },
})
</script>
