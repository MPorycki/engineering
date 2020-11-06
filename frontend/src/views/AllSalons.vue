<template>
    <myForm>
        <h2>Nasze salony</h2>

           <table class="col text-center" id="myTable" v-for="salon in salons" :key="salon.salon_id">
                    <td id="date">
                        {{parseAddress(salon.address)}}
                    </td>
                    <td >
                        {{salon.opening_hour + " - " + salon.closing_hour}}
                    </td>
                    <td >
                        <a target="_blank" :href="googleMapsLink(salon.address)">Mapa</a>
                    </td>
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
    }

    #tblrow {
        height: 50px;
        width: 100%;
    }

    #date{
        padding-right: 100px;
        padding-left:25px;
        padding-top:10px;
    }
</style>