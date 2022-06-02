<template>

  <div  class="fill-height home">
    <div class="row justify-content-center fixed-top pb-5 bg-black m-5" id="search_row" style="--bs-bg-opacity: .4;position:fixed; top:5vh; height: 83vh">
        <div class="col-6 my-2 text-center py-2 mt-2 opacity-70" style="max-height: 90vh;">
          <h1 class="text-white display-4 font-weight-bold mb-4" style="font-size:11em; font-weight:900">Điro</h1>
          <h1 class="text-white display-4 font-weight-bold mb-4" style="font-size:3em;" > Aplikacija za lako iznajmljivanje automobila</h1>
            <div class="d-flex">
              
              <input class="form-control me-2" type="search" placeholder="Enter a destiantion" aria-label="Search" id="searchbar" required>
              <input type="date" class="me-2" name="date" id="date" style="width:250px;" required/>
              <button class="btn btn-light btn-outline-secondary" id="search" @click="search()">Search</button>
              
            </div>
            <div class="d-flex filteri mt-1 d-none">
              <input class="form-control me-2" type="text" placeholder="Godiste" id="godiste">
              <input class="form-control me-2" type="text" placeholder="Marka" id="marka">
              <input class="form-control me-2" type="text" placeholder="Model" id="model">
            </div>
        </div>
        <div class="d-flex filteri mt-1 d-none">
          <input
            class="form-control me-2"
            type="text"
            placeholder="Godiste"
            id="godiste"
          />
          <input
            class="form-control me-2"
            type="text"
            placeholder="Marka"
            id="marka"
          />
          <input
            class="form-control me-2"
            type="text"
            placeholder="Model"
            id="model"
          />
        </div>
    </div>
  </div>
</template>

<style scoped>


  .home{
    background-image: url("@/assets/naslovna1a.jpeg");
    min-height: 92.5vh; 
    background-size: cover !important;
    top: 10vh;
  }
</style>

<script>

export default {
  name: "HomeView",
  //components: { CarCard },
  methods:{
    search(){
      this.$router.push('listing')
    }
  }
};
</script>
