<template>
  <div
    ref="mapContainer"
    style="position: relative; width: 600px; height: 400px"
  ></div>
</template>

<script>
import Config from "./config.js";
import SVG from "./pin.svg";
export default {
  name: "MapComponent",
  props: ["coords", "center"],
  data() {
    return {
      apiLoaded: false,
      map: null,
      map_coords: this.coords,
      map_center: this.center,
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
            //delete window[self.getInitCallbackFnName()];
            self.apiLoaded = true;
            resolve();
          };
          let tag = document.createElement("script");
          tag.type = "text/javascript";
          tag.src = self.getMapApiUrl();
          tag.async = true;
          tag.defer = true;
          tag.onerror = function (event) {
            //delete window[self.getInitCallbackFnName()];
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
            //console.log(self.map_center);
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
    console.log(this.map_coords);
    this.render();
  },
};
</script>
