<template>
    <myForm>
        <h2>Nasze usługi</h2>
        <table class="col text-center" id="myTable" v-for="service in services" :key="service.id">
            <router-link tag="tr" id="tblrow" class="btn btn-light shadow" :to="{ path: 'serviceDetails', query: { id: service.id }}">
                <td id="serviceName">
                    {{service.name}}
                </td >
                <td id="servicePrice">
                    {{service.price}} PLN
                </td>
                <td id="serviceDuration">
                    {{service.service_duration}} min
                </td>
            </router-link>
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
    data() {
        return {
            services: [],
        }
    },
    mounted(){
        axios.get(this.$backend_url + "service/").then(res => this.setServices(res.data["Services"]))
    },
    methods: {
        setServices(servicesInput){
            console.log(servicesInput)
            for (var i=0; i < servicesInput.length; i++) {
                this.services.push(servicesInput[i])
            }
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
        padding-top: 10px;
    }

    #serviceName{
        width:50%;
        font-size: -1.2vw;
        text-align: left;
    }

    #servicePrice {
        width:15%;
        font-size: -1.2vw;
        text-align: left;
    }

    #serviceDuration {
        width: 12%;
        padding-left:5px;
        font-size: -1.2vw;
        text-align: left;
    }
</style>