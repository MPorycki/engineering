<template>
    <myForm>
        <h2>Moje wizyty</h2>
        <router-link v-if="this.isHairdresser == false" to='/visitCreate' class="btnSubmit" >
        Umów wizytę 
        </router-link>
        <table class="col text-center" id="myTable" v-for="visit in visits" :key="visit.visit_id">
            <router-link tag="tr" :style="[visit.visit_status=='FINISHED' ? {'background': '#D8D8D8'} : {'background': '#FFF'}]" id="tblrow" class="btn btn-light shadow" :to="{ path: 'visitDetails', query: { id: visit.visit_id }}">
                <td id="date">
                    {{visit.visit_date}}
                </td>
                <td >
                    {{visit.visit_data}}
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
    data(){
        return {
            visits: [],
            isHairdresser: false
        }
    },
    mounted(){
        var config = { headers: {account_id: this.$cookies.get('user-id'), session_id: this.$cookies.get('session-id')}}
        axios.get(this.$backend_url + "accountVisits/" + this.$cookies.get('user-id'), config).then(res => this.setVisits(res.data["visits"]))
        axios.get(this.$backend_url + "employee_access/", config).then(res => this.setAccess(res.data)).catch(() => this.handleAccessError())
    },
    methods: {
        setVisits(visitsInput){
            for (var i=0; i < visitsInput.length; i++) {
                this.visits.push(visitsInput[i])
            }
        },
        setAccess(accessResults){
            this.isHairdresser = accessResults.isHairdresser
        },
        handleAccessError(){}
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