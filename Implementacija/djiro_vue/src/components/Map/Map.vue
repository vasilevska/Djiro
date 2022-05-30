<template>
    <div ref="mapContainer" style="position:relative;width:600px;height:400px;">
    </div>
</template>

<script>
import Config from './config.js'
    export default{
        name: 'MapComponent',
        data() {
        return {
            apiLoaded: false,
            map: null
        }
        },
        methods: {
            libLoaded() {
                return !!(window.Microsoft && window.Microsoft.Maps && window.Microsoft.Maps.Map);
            },
            getInitCallbackFnName(){
                return 'getMap';
            },
            getMapApiUrl(){
                var bingMapUrl = Config.bingApiUrl;
                return bingMapUrl.replace('{callback}', this.getInitCallbackFnName());                
            },
            loadApi() {
                let self = this
                return new Promise((resolve, reject) => {
                    if(self.libLoaded()){
                        self.apiLoaded = true;
                        resolve();
                    } else {
                        window[self.getInitCallbackFnName()] = function() {
                            //delete window[self.getInitCallbackFnName()];
                            self.apiLoaded = true;
                            resolve();
                        };
                        let tag = document.createElement('script');
                        tag.type = 'text/javascript';
                        tag.src = self.getMapApiUrl();
                        tag.async = true;
                        tag.defer = true;
                        tag.onerror = function(event) {
                            //delete window[self.getInitCallbackFnName()];
                            reject(event);                            
                        };
                        document.head.append(tag);
                    }
                });
            },
            render(){
                return new Promise((resolve, reject) => {
                    Promise.all([this.loadApi()]).then(() => {
                        this.map = new Microsoft.Maps.Map(this.$refs.mapContainer, {
                            credentials: Config.credentials,
                            center: new Microsoft.Maps.Location(51.50632, -0.12714),
                            mapTypeId: Microsoft.Maps.MapTypeId.aerial,
                            zoom: 10
                        });
                        resolve();
                    }).catch(function(err){
                        reject(err);
                    }).finally(() => {
                        this.rendering = false;
                    });
                });
            }
        },
    mounted(){
        this.render();
    }
    }


</script>