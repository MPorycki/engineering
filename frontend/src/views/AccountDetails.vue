<template>
    <div>
        <myForm>
            <H2>Szczegóły konta</H2>
            <h5><strong>Imię</strong></h5>
            <p>{{details.firstName}}</p>
            <h5><strong>Nazwisko</strong></h5>
            <p>{{details.lastName}}</p>
            <h5><strong>Email</strong></h5>
            <p>{{details.email}}</p>
        </myForm>
        <myForm>
        <h2>Moje wizyty</h2>
            <router-link v-if="this.isHairdresser == false" to='/visitCreate' class="btnSubmit" >
            Umów wizytę 
            </router-link>
            <table class="col text-center" id="myTable" v-for="visit in visits" :key="visit.visit_id">
                <router-link tag="tr" id="tblrow" class="btn btn-light shadow" :to="{ path: 'visitDetails', query: { id: visit.visit_id }}">
                    <td id="date">
                        {{visit.visit_date}}
                    </td>
                    <td >
                        {{visit.visit_data}}
                    </td>
                </router-link>
            </table>
    </myForm>
    </div>
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
            details: [],
            id: "",
            isHairdresser: false,
            visits: []
        }
    },
    mounted(){
        var config = { headers: {account_id: this.$cookies.get('user-id'), session_id: this.$cookies.get('session-id')}}
        axios.get(this.$backend_url + "account/" + this.$route.query.id, config).then(res => this.setDetails(res.data))
        axios.get(this.$backend_url + "accountVisits/" + this.$route.query.id, config).then(res => this.setVisits(res.data["visits"]))
        axios.get(this.$backend_url + "employee_access/", config).then(res => this.setAccess(res.data)).catch(() => this.handleAccessError())
    },
    methods: {
        setDetails(data){
            this.details = data
        },
        setAccess(accessResults){
            this.isHairdresser = accessResults.isHairdresser
        },
        handleAccessError(){},
        setVisits(visitsInput){
            for (var i=0; i < visitsInput.length; i++) {
                this.visits.push(visitsInput[i])
            }
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