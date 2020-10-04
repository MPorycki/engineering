<template>
    <div>
        <myForm>  
            <h3>Zarezerwuj wizytę</h3>
                <form @submit.prevent="createVisit">
                    <div class="form-group">
                        <label for="formControlSelect1">Wybierz salon</label>
                            <select class="form-control" id="formControlSelect1" v-model="salonSelected" @change="onSalonSelect()">
                                <option v-for="salon in salons" :value="salon" :key="salon.id">{{parseAdress(salon.address)}}</option>
                            </select>
                    </div>
                    <div class="form-group">
                        <label for="formControlSelect2">Wybierz fryzjera</label>
                            <select class="form-control" id="formControlSelect2" v-model="hairdresserSelected" @change="onHairdresserSelect()">
                                <option v-for="hairdresser in hairdressers" :value="hairdresser" :key="hairdresser.id">{{hairdresser.firstName + " " + hairdresser.lastName}}</option>
                            </select>
                    </div>
                    <div class="form-group" v-if="hairdresserSelected != null">
                        <label for="exampleFormControlSelect1">Wybierz usługi</label>
                            <div class="form-check" v-for="service in services" :key="service.id"  @change="onServiceSelect()">
                                <input class="form-check-input" type="checkbox" :id="service.name" :value=service v-model="servicesSelected">
                                <label class="form-check-label" :for="service.name">{{service.name + " - " + service.price + " PLN"}}</label>
                            </div>
                            <p v-if="servicesSelected.length > 0"><b>Szacowany czas usługi to {{calculateServiceTime()}} minut.</b></p>
                    </div>
                    <div class="form-group" v-if="servicesSelected.length > 0">
                        <label for="date">Wybierz dzień wizyty</label>
                        <datepicker id="date" :language="pl" v-model="dateSelected" @selected="loadHours()" format="dd/MM/yyyy" :disabled-dates="disabledDates" :bootstrap-styling="true"></datepicker>
                    </div>
                    <div class="form-group" v-if="suggestedHours != null">
                        <label for="myTable">Dostępne godziny wizyty</label>
                        <table class="col text-center" id="myTable">
                            <tr id="tblrow" v-for="i in Math.ceil(suggestedHours.length / 3)" :key="i">
                                <td >
                                    <button @click="setHourSelected({hour})" :id="'H'+hour" style="margin-right: 15px" type="button" class="btn btn-outline-primary" v-for="hour in suggestedHours.slice((i - 1) * 3, i * 3)" :key="hour">{{hour}}</button>
                                </td>
                            </tr>
                        </table>
                    </div>
                    <div class="form-group">
                        <input v-if="hourSelected != null" type="submit" class="btnSubmit" value="Zarezerwuj" />
                    </div>
                </form> 
        </myForm>
    </div>
</template>

<script>
import myForm from '../components/myForm'

import axios from 'axios'
import datepicker from 'vuejs-datepicker' // https://www.npmjs.com/package/vuejs-datepicker
import pl from 'vuejs-datepicker/dist/locale'
import moment from 'moment'
export default {
    components: {
        myForm,
        datepicker
    },
    data() {
        return {
            salons: [],
            salonSelected: null,
            hairdressers: [],
            hairdresserSelected: null,
            services: [],
            servicesSelected: [],
            dateSelected: new Date().toLocaleString(),
            pl: pl,
            disabledDates:{to: new Date()},
            suggestedHours: null,
            hourSelected: null
        }
    },
    methods: {
        getSalons(){
            axios.get(this.$backend_url  + "salon/").then(res => this.salons = res.data["Salons"])
        },
        parseAdress(adressDict){
            return adressDict["city"] + ", " + adressDict["street"] + " " + adressDict["building_no"]
        },
        onSalonSelect(){
            this.getHairdressers(this.salonSelected.id)
            this.hairdresserSelected = null
        },
        getHairdressers(salonId){
            axios.get(this.$backend_url + "hairdresser/"+salonId).then(res => this.hairdressers = res.data["hairdressers"])
        },
        getServices(){
            axios.get(this.$backend_url + "service/").then(res => this.services = res.data["Services"])
        },
        onHairdresserSelect(){
            this.getServices()
        },
        onServiceSelect(){
            console.log(this.servicesSelected)
        },
        calculateServiceTime(){
            var sum = 0;
            var service;
            for (service of this.servicesSelected){
                sum += service.service_duration
            }
            return sum
        },
        loadHours(){
            var data = {
                "date": moment(this.dateSelected).format('DD/MM/YYYY').split(",")[0],
                "customerId": "ba0ea3715a514c52b2d8c6c917bec629", // TODO ogarnac zeby nie bylo na sztywno wpisane
                "hairdresserId": this.hairdresserSelected.id,
                "serviceDuration": this.calculateServiceTime(),
                "salonId": this.salonSelected.id,
            }
            axios.post(this.$backend_url +"visit/availability/", data).then(res => this.renderHourButtons(res.data["availableHours"]))
        },
        renderHourButtons(hours){
            this.suggestedHours = hours
        },
        setHourSelected(hour){
            if (this.hourSelected == null){
                this.hourSelected = hour.hour
                document.getElementById("H"+this.hourSelected).classList.add('btn-primary');

                document.getElementById("H"+this.hourSelected).classList.remove('btn-outline-primary');
            } else {
                document.getElementById("H"+this.hourSelected).classList.remove('btn-primary');

                document.getElementById("H"+this.hourSelected).classList.add('btn-outline-primary');

                this.hourSelected = hour.hour
                document.getElementById("H"+this.hourSelected).classList.add('btn-primary');

                document.getElementById("H"+this.hourSelected).classList.remove('btn-outline-primary');
            }
        },
        createVisit(){
            if (this.validateData()){
                var data = {
                    "visit_date_start": moment(this.dateSelected).format('DD/MM/YYYY').split(",")[0] + " " + this.hourSelected,
                    "customer_id": "ba0ea3715a514c52b2d8c6c917bec629", // TODO ogarnac zeby nie bylo na sztywno wpisane
                    "hairdresser_id": this.hairdresserSelected.id,
                    "service_duration": this.calculateServiceTime(),
                    "salon_id": this.salonSelected.id,
                    "services": this.servicesSelected
                }
                axios.post(this.$backend_url +"visit/", data).then(res => this.handleCreationSuccess(res.data)).catch(res => alert(res.response.data.hairdresser_taken))
            } else{
                alert("Uzupełnij wszystkie pola")
            }
        },
        validateData(){
                if (this.hairdresserSelected == null || this.calculateServiceTime() == 0 || this.salonSelected == null || this.servicesSelected.length == 0){ // TODO add customer id
                    return false
                }
            return true
        },
        handleCreationSuccess(data){
            if (data.success){
                this.$router.push({ name: 'AllVisits', })
            } 
        }
    },
    mounted(){
        this.getSalons();
    }
    
}
</script>

<style scoped>
    #tblrow td {
        margin-right: 10px;
    }
</style>