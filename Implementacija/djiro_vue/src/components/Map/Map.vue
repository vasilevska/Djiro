<template>
<div class="col-auto justify-content-center align-items-center">
    <div v-if="rendering" class="text-center">
    <ring-loader :color="color1" :height="height"></ring-loader>
    </div>
    <div 
    v-else
    ref="mapContainer"
    class= "v-100"
  ></div>
</div>
</template>

<script>
import Config from "./config.js";
import SVG from "./pin.svg";
import RingLoader from 'vue-spinner/src/RingLoader.vue'

export default {
  name: "MapComponent",
  props: ["coords", "center"],
  data() {
    return {
      apiLoaded: false,
      map: null,
      map_coords: this.coords,
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
      return new Promise((resolve, reject) => {
        Promise.all([self.loadApi()])
          .then(() => {
            var centr = new Microsoft.Maps.Location(
              self.map_center["lat"],
              self.map_center["long"]
            );

            this.map = new Microsoft.Maps.Map(this.$refs.mapContainer, {
              credentials: Config.credentials,
              center: centr,
              mapTypeId: Microsoft.Maps.MapTypeId.aerial,
              zoom: 12,
              disableScrollWheelZoom: true,
              mapTypeId: Microsoft.Maps.MapTypeId.road,
              disableStreetside: true,
              showZoomButtons: false,
              showLocateMeButton: false,
              disableMapTypeSelectorMouseOver: true,
              disableStreetside: true,
              showMapTypeSelector: false,
            });

            self.map.entities.push(
              new Microsoft.Maps.Pushpin(centr, {
                icon: SVG,
                anchor: new Microsoft.Maps.Point(0, 0),
              })
            );

            for (var coord of this.map_coords) {
              var center = new Microsoft.Maps.Location(
                coord["lat"],
                coord["long"]
              );
              var pin = new Microsoft.Maps.Pushpin(center, {
                icon: SVG,
                anchor: new Microsoft.Maps.Point(0, 0),
              });
              this.map.entities.push(pin);
            }

            resolve();
          })
          .catch(function (err) {
            reject(err);
          })
          .finally(() => {
            this.rendering = false;
          });
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
