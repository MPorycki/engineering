<template>
    <myForm>
        <h2>Nasze salony</h2>
           <table class="col text-center" id="myTable" v-for="salon in salons" :key="salon.salon_id">
               <tr class="shadow" id="tblrow">
                    <td id="address">
                        {{parseAddress(salon.address)}}
                    </td>
                    <td id="openHours">
                        {{salon.opening_hour + " - " + salon.closing_hour}}
                    </td>
                    <td id="map">
                        <a target="_blank" :href="googleMapsLink(salon.address)">Mapa</a>
                    </td>
                </tr>
            </table>
    </myForm>
</template>


<script>
import myForm from '../components/myForm'

import axios from 'axios'
export default {
     components: {
        myForm
    },
    data(){
        return {
            salons: []
        }
    },
    mounted(){
        axios.get(this.$backend_url + "salon/").then(res => this.setSalons(res.data["Salons"]))
    },
    methods: {
        setSalons(salonsInput){
            console.log(salonsInput)
            for (var i=0; i < salonsInput.length; i++) {
                this.salons.push(salonsInput[i])
            }
        },
        parseAddress(address){
            return address["city"] + ", " + address["street"] + " " + address["building_no"]
        },
        googleMapsLink(address){
            var url = "https://www.google.com/maps/search/?api=1&"
            var parameters = "query=" + address["city"] + "+" + address["street"] + "+" + address["building_no"]
            return url+parameters
        }
    }
}
</script>

<style scoped>
    #myTable {
      margin-top: 25px;
      table-layout: fixed;
    }

    #tblrow {
        height: 50px;
        width: 100%;
        display: grid;
        grid-template-columns: 60% 25% 15%
    }

    #address{
        padding-top:10px;
        padding-left: 10px;
        grid-column: 1;
        font-size: -1.2vw;
        width:100%;
        text-align: left;
    }

    #openHours {
        padding-top:10px;
        grid-column: 2;
        font-size: -1.2vw;
        width:100%;
        text-align: left;
    }

    #map {
        padding-top:10px;
        grid-column: 3;
        font-size: -1.2vw;
        width:100%;
        text-align: center;
    }
</style>