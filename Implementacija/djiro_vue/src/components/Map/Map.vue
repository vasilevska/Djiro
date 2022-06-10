/* eslint-disable */
<template>
<div class="col-auto justify-content-center align-items-center omotac">
    <div v-if="rendering" class="text-center">
    <ring-loader :color="color1" :height="height"></ring-loader>
    </div>
    <div 
    v-show="!rendering"
    ref="mapContainer"
    class= "v-100"
  ></div>
</div>
</template>

<style scoped>
  .omotac{
    width:100%;
    height: 100%;
  }
</style>

<script>
import Config from "./config.js";
import SVG from "./pin.svg";
import RingLoader from 'vue-spinner/src/RingLoader.vue'

export default {
  name: "MapComponent",
  props: ["cars", "center", "zoom"],
  data() {
    return {
      apiLoaded: false,
      map: null,
      map_center: this.center,
      rendering : true,
      color1: '#3AB982',
      height: '70px'
    };
  },
  methods: {
    libLoaded() {
      return !!(
        window.Microsoft &&
        window.Microsoft.Maps &&
        window.Microsoft.Maps.Map
      );
    },
    getInitCallbackFnName() {
      return "getMap";
    },
    getMapApiUrl() {
      var bingMapUrl = Config.bingApiUrl;
      return bingMapUrl.replace("{callback}", this.getInitCallbackFnName());
    },
    loadApi() {
      let self = this;
      return new Promise((resolve, reject) => {
        if (self.libLoaded()) {
          self.apiLoaded = true;
          resolve();
        } else {
          window[self.getInitCallbackFnName()] = function () {
            self.apiLoaded = true;
            resolve();
          };
          let tag = document.createElement("script");
          tag.type = "text/javascript";
          tag.src = self.getMapApiUrl();
          tag.async = true;
          tag.defer = true;
          tag.onerror = function (event) {
            reject(event);
          };
          document.head.append(tag);
        }
      });
    },
    render() {
      let self = this;
        Promise.all([self.loadApi()])
          .then(() => {
            var centr = new Microsoft.Maps.Location(
              self.map_center["lat"],
              self.map_center["long"]
            );

            self.map = new Microsoft.Maps.Map(self.$refs.mapContainer, {
              credentials: Config.credentials,
              center: centr,
              mapTypeId: Microsoft.Maps.MapTypeId.aerial,
              zoom: self.zoom,
              disableScrollWheelZoom: true,
              mapTypeId: Microsoft.Maps.MapTypeId.road,
              disableStreetside: true,
              //showZoomButtons: false,
              showLocateMeButton: false,
              disableMapTypeSelectorMouseOver: true,
              disableStreetside: true,
              showMapTypeSelector: false,
            });

            for (var car of this.cars) {
              var center = new Microsoft.Maps.Location(
                car.lat,
                car.long
              );
              var pin = new Microsoft.Maps.Pushpin(center, {
                icon: SVG,
                anchor: new Microsoft.Maps.Point(50,72)
              });
              this.map.entities.push(pin);
            }
          })
          .catch(err => {
            console.log(err);
          })
          .finally(() => {
            this.rendering = false;
          });

    },
  },
  mounted() {
    this.rendering = true;
    this.render();
  },
  components:{
    RingLoader
  }
};
</script>
