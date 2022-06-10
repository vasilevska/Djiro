<template>
  <div class="box">
    <div class="container">
      <div class="row">
        <div class="col-4">
          <img v-bind:src="car.get_thumbnail" />
        </div>
        <div class="col-4">
          <h3 class="id-size-4">Model: {{ car.model.name }}</h3>
          <h3 class="id-size-4">Type: {{ car.type }}</h3>
          <!-- TODO: Fali ocena, treba i ovde posebna komponenta -->

          <hr />
          <div class="row align-bottom">
            <div class="col-3">
              <button class="btn btn-primary">
                <router-link v-bind:to="car.get_absolute_url">
                  Više detalja</router-link
                >
              </button>
            </div>
            <div class="col-3 align-right">
              <h3 class="id-size-4">
                &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;{{
                  car.price_per_day
                }}€/dan
              </h3>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
export default {
  name: "CarCard",
  setup() {},
  props: ["car"],
};
</script>
<style scoped>
.btn-primary {
  width: 150px;
}
.box {
  padding: 10px;
}

router-link {
  color: white;
}
</style>
