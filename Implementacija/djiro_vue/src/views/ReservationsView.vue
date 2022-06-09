<template>
  <div class="div container pt-5">
    <ul class="nav nav-tabs" id="tabs">
      <li class="nav-item">
        <a
          class="nav-link active"
          aria-current="page"
          href="#tab-01"
          aria-controls="tab-01"
          role="tab"
          data-bs-toggle="tab"
          >Aktivne</a
        >
      </li>
      <li class="nav-item">
        <a
          class="nav-link"
          href="#tab-02"
          aria-controls="tab-02"
          role="tab"
          data-bs-toggle="tab"
          >Na čekanju</a
        >
      </li>
      <li class="nav-item">
        <a
          class="nav-link"
          href="#tab-03"
          aria-controls="tab-03"
          role="tab"
          data-bs-toggle="tab"
          >Prošle</a
        >
      </li>
    </ul>
    <div class="row tab-content">
      <div role="tabpanel" class="col-4 tab-pane active" id="tab-01">
        <h3 name="title">Aktivne rezervacije</h3>
        <ReservationsActive />
      </div>
      <div role="tabpanel" class="tab-pane active col-4" id="tab-02">
        <h3 name="title">Rezervacije na čekanju</h3>
        <ReservationsRequested />
      </div>
      <div role="tabpanel" class="tab-pane active col-4" id="tab-03">
        <h3 name="title">Prošle rezervacije</h3>
        <ReservationsFinished />
      </div>
    </div>
  </div>
</template>

<script>
import ReservationsRequested from "../components/ReservationCardsRequested.vue";
import ReservationsActive from "../components/ReservationCardsActive.vue";
import ReservationsFinished from "../components/ReservationCardsFinished.vue";
import $ from "jquery";
export default {
  name: "ReservationsView",
  components: {
    ReservationsRequested,
    ReservationsActive,
    ReservationsFinished,
  },
  mounted() {
    this.display_change();
    $(window).on("resize", this.display_change);
  },
  methods: {
    display_change() {
      if ($(window).width() < 1200) {
        $("#tabs").show();
        $('h3[name="title"]').hide();
        $("#tab-02").removeClass("active");
        $("#tab-03").removeClass("active");
        $("#tab-02").removeClass("col-4");
        $("#tab-03").removeClass("col-4");
        $("#tab-01").removeClass("col-4");
      } else {
        $("#tabs").hide();
        $('h3[name="title"]').show();
        $("#tab-02").addClass("active");
        $("#tab-03").addClass("active");
        $("#tab-01").addClass("active");
        $("#tab-02").addClass("col-4");
        $("#tab-03").addClass("col-4");
        $("#tab-01").addClass("col-4");
      }
    },
  },
};
</script>
