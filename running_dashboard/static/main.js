import 'ol/ol.css';
import {Map, View} from 'ol';
import TileLayer from 'ol/layer/Tile';
import VectorLayer from 'ol/layer/Vector';
import VectorSource from 'ol/source/Vector';
import Style from 'ol/style/Style'
import Stroke from 'ol/style/Stroke'
import Fill from 'ol/style/Fill'
import GeoJSON from 'ol/format/GeoJSON';
import OSM from 'ol/source/OSM'
// import proj from 'ol/proj'

var run_data = document.getElementById("data").innerHTML;
var format = new GeoJSON();
var features = format.readFeatures(JSON.parse(run_data));

var map = new Map({
  target: 'map',
  layers: [
    new TileLayer({
      source: new OSM()
    }),
    // new TileLayer({
    //   source: new XYZ({
    //     url: 'https://{a-c}.tile.openstreetmap.org/{z}/{x}/{y}.png'
    //   })
    // }),
    // new VectorLayer({
    //   source: new VectorSource({
    //     features: features
    //   })
    // }),
  ],
  view: new View({
    center:[3883169.62, 3775225.09],
    // center: proj.fromLonLat([34.883106, 32.090721]),
    zoom: 14
  })
});

var run_style = new Style({
  fill: new Fill({
    color: [0,0,0,1.0],
  }),
  stroke: new Stroke({
    color: [0,0,255,1.0],
    width: 4,
    lineJoin: 'round'
  })
})

var run_layer =  new VectorLayer({
      source: new VectorSource({
          features: features
      }),
      style: run_style
  })


map.addLayer(run_layer);