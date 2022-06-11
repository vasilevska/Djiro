<template>
  <Transition name="modal">
    <div v-if="show" class="modal-mask">
      <div class="modal-wrapper">
        <div class="modal-container">
          <div class="modal-header">Oceni automobil</div>

          <div class="modal-body">
            <form id="ratingForm">
              <input type="number" min="1" max="5" name="car_rating" id="car_rating" />
              <textarea name="descr" id="descr"></textarea>
              <input type="number" min="1" max="5" name="djiler_rating" id="djiler_rating" />
              <textarea name="descr_djiler" id="descr_djiler"></textarea>
              <input
                type="number"
                name="idr"
                :value="reservation.idr"
                id="idr"
                class="d-none"
              />
              <input
                type="number"
                name="idd"
                :value="reservation.idd.pk"
                id="idd"
                class="d-none"
              />
              <input
                type="number"
                name="idu"
                :value="reservation.idu.pk"
                id="idu"
                class="d-none"
              />
              <input
                type="number"
                name="idc"
                :value="reservation.idc"
                id="idc"
                class="d-none"
              />
            </form>
          </div>

          <div class="modal-footer">
            <slot name="footer">
              <button
                class="modal-default-button"
                @click="
                  sendRating();
                  $emit('close');
                "
              >
                Oceni
              </button>
            </slot>
          </div>
        </div>
      </div>
    </div>
  </Transition>
</template>

<script>
import axios from "axios";

export default {
  props: {
    show: Boolean.apply,
    reservation: null,
  },
  methods: {
    sendRating() {
      console.log("ocenjeno");
      console.log(this.reservation.idd.pk);
      var formElement = document.querySelector("form");
      var formData = new FormData(formElement);
      var object = {};
      formData.forEach((value, key) => (object[key] = value));
      var json = JSON.stringify(object);
      console.log(object);
      new Promise((resolve) => {
        axios({
          method: "post",
          url: `http://127.0.0.1:8000/api/ratings/car/${this.reservation.idu.pk}`,
          data: json,
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${this.$store.state.accessToken}`,
          },
        })
          .then((response) => {
            console.log(response.data);
            resolve();
          })
          .catch((err) => {
            console.log(err);
            resolve();
          });
      });
    },
  },
};
</script>

<style>
.modal-mask {
  position: fixed;
  z-index: 9998;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: table;
  transition: opacity 0.3s ease;
}

.modal-wrapper {
  display: table-cell;
  vertical-align: middle;
}

.modal-container {
  width: 300px;
  margin: 0px auto;
  padding: 20px 30px;
  background-color: #fff;
  border-radius: 2px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.33);
  transition: all 0.3s ease;
}

.modal-header h3 {
  margin-top: 0;
}

.modal-body {
  margin: 20px 0;
}

.modal-default-button {
  float: right;
}

/*
 * The following styles are auto-applied to elements with
 * transition="modal" when their visibility is toggled
 * by Vue.js.
 *
 * You can easily play with the modal transition by editing
 * these styles.
 */

.modal-enter-from {
  opacity: 0;
}

.modal-leave-to {
  opacity: 0;
}

.modal-enter-from .modal-container,
.modal-leave-to .modal-container {
  -webkit-transform: scale(1.1);
  transform: scale(1.1);
}
</style>
