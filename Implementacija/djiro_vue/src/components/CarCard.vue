<template>
  <div class="row mt-5">
    <div class="col-sm-4">
      <div class="card">
        <img
          class="card-img-top"
          width="100%"
          v-bind:src="images[0]"
        />
        <div class="card-body pt-0 px-0">
          <div class="d-flex flex-row justify-content-between mb-0 px-3">
            <small class="text-muted mt-1">Price per day:</small>
            <h6>&dollar;{{ carInfo.pricePerDay }}&ast;</h6>
          </div>
          <hr class="mt-2 mx-3" />
          <div class="d-flex flex-row justify-content-between px-3 pb-4">
            <div class="d-flex flex-column">
              <span class="text-muted">Fuel Efficiency</span
              ><small class="text-muted">L/100KM&ast;</small>
            </div>
            <div class="d-flex flex-column">
              <h5 class="mb-0">8.5/7.1</h5>
              <small class="text-muted text-right">(city/Hwy)</small>
            </div>
          </div>
          <div class="d-flex flex-row justify-content-between p-3 mid">
            <div class="d-flex flex-column">
              <small class="text-muted mb-1">ENGINE</small>
              <div class="d-flex flex-row">
                <img
                  src="https://imgur.com/iPtsG7I.png"
                  width="35px"
                  height="25px"
                />
                <div class="d-flex flex-column ml-1">
                  <small class="ghj">1.4L MultiAir</small
                  ><small class="ghj">16V I-4 Turbo</small>
                </div>
              </div>
            </div>
            <div class="d-flex flex-column">
              <small class="text-muted mb-2">HORSEPOWER</small>
              <div class="d-flex flex-row">
                <img src="https://imgur.com/J11mEBq.png" />
                <h6 class="ml-1">135 hp&ast;</h6>
              </div>
            </div>
          </div>
          <small class="text-muted key pl-3">Standard key Features</small>
          <div class="mx-3 mt-3 mb-2">
            <button type="button" class="btn btn-dark btn-block">
              <small>Request reservation</small>
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<style>
body {
  background: #f5f1ee;
  font-family: "Roboto", sans-serif;
}
.card {
  width: 250px;
  border-radius: 10px;
}

.card-img-top {
  border-top-right-radius: 10px;
  border-top-left-radius: 10px;
}
span.text-muted {
  font-size: 12px;
}
small.text-muted {
  font-size: 8px;
}
h5.mb-0 {
  font-size: 1rem;
}
small.ghj {
  font-size: 9px;
}
.mid {
  background: #ecedf1;
}
h6.ml-1 {
  font-size: 13px;
}
small.key {
  text-decoration: underline;
  font-size: 9px;
  cursor: pointer;
}
.btn-danger {
  color: #ffcbd2;
}
.btn-danger:focus {
  box-shadow: none;
}
small.justify-content-center {
  font-size: 9px;
  cursor: pointer;
  text-decoration: underline;
}

@media screen and (max-width: 600px) {
  .col-sm-4 {
    margin-bottom: 50px;
  }
}
</style>
<script>
export default {
  name: "CarCard",
  setup() {},
  props: ["carInfo"],
};
</script>
