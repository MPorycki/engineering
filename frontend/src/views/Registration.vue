<template>
    <div class="container login-container" >
            <div class="row">
                <div class="col-md-6 login-form">
                    <h3>Rejestracja</h3>
                    <form @submit.prevent="register">
                        <div class="form-group">
                            <input type="text" id="email" class="form-control" placeholder="Podaj swój email" value="" />
                            <b-tooltip target="email" id="email_error" class="rtooltips" triggers="hover" placement="right"  :disabled=true >{{email_text}}</b-tooltip>
                        </div>
                        <div class="form-group">
                            <input type="text" id="first_name" class="form-control" placeholder="Podaj swoje imię" value="" />
                            <b-tooltip target="first_name" id="first_name_error" class="rtooltips" triggers="hover" placement="right"  :disabled=true>{{first_name_text}}</b-tooltip>
                        </div>
                        <div class="form-group">
                            <input type="text" id="last_name" class="form-control" placeholder="Podaj swoje nazwisko" value="" />
                            <b-tooltip target="last_name" id="last_name_error" class="rtooltips" triggers="hover" placement="right"  :disabled=true>{{last_name_text}}</b-tooltip>
                        </div>
                        <div class="form-group">
                            <input type="password" id="password" class="form-control" placeholder="Wpisz hasło" value="" />
                            <b-tooltip target="password" id="password_error" class="rtooltips" triggers="hover" placement="right"  :disabled=true>{{password_text}}</b-tooltip>
                        </div>
                        <div class="form-group">
                            <input type="password" id="password_confirm" class="form-control" placeholder="Potwierdź hasło" value="" />
                        </div>
                        <div class="form-group">
                            <input type="submit" class="btnSubmit" value="Zarejestruj się"/>
                        </div>
                    </form>
                </div>
            </div>
        </div>
</template>

<script>
import axios from 'axios'

export default {
    name: 'Registration',
    data()
        {
        return {tooltip_email_show: false, email_text: "", first_name_text: "", last_name_text:"", password_text: ""}
        }
    ,
    methods: {
    register(){
            var data = {
                email:document.getElementById("email").value,
                first_name: document.getElementById("first_name").value,
                last_name: document.getElementById("last_name").value,
                raw_password: document.getElementById("password").value,
                account_type: "customer",
                salon_id: ""
            }
            if (this.validate_form(data)){
                axios.post(this.$backend_url + "account/", data).then(res => this.register_success(res.data)).catch(error => this.handle_error(error.response.data));
            }
        },
        register_success(message){
            alert(message);
            this.$router.push({ name: 'Login', })
        },
        handle_error(error_data){
            if (error_data["email_taken"]) {
                this.add_error("email_error", "Podany mail jest zajety");
            }
        },
        validate_form(data){
            var val_email = this.validate_email(data["email"])
            var val_fname = this.validate_name(data["first_name"])
            var val_lname = this.validate_last_name(data["last_name"])
            var val_pass = this.validate_password(data["raw_password"], document.getElementById("password_confirm").value)
            if (val_email && val_fname && val_lname && val_pass){
                return true;
            } else {
                return false;
            }

        },
        validate_email(email){
            var email_regex = /.*@.*\.[a-z]{2,}/;
            if ((email.replace(/\s/g, '')).length == 0) {
                this.add_error("email", "Email jest wymagany do rejestracji")
                return false;
            }
            else if (!email_regex.test(email)){
                this.add_error("email", "Niepoprawny format maila")
                return false;
            } else {
                this.clear_error("email")
                return true
            }
        },
        validate_name (first_name){
            var name_regex = /[A-Z]?[a-z]*/;
            if ((first_name.replace(/\s/g, '')).length == 0){
                this.add_error("first_name", "Imię jest wymagane do rejestracji")
                return false;
            } else if  ((first_name.replace(/\s/g, '')).length > 32) {
                this.add_error("first_name", "Maksymalna ilość znaków to 32.")
                return false;
            } else if (!name_regex.test(first_name)){
                this.add_error("first_name", "W imieniu można korzystać tylko z liter")
                return false;
            } else {
                this.clear_error("first_name")
                return true;
            }
        },
        validate_last_name(last_name){
             var last_name_regex = /[A-Z]?[a-z]*/;
            if ((last_name.replace(/\s/g, '')).length == 0){
                this.add_error("last_name", "Nazwisko jest wymagane do rejestracji")
                return false;
            } else if  ((last_name.replace(/\s/g, '')).length > 32) {
                this.add_error("last_name", "Maksymalna ilość znaków to 32.")
                return false;
            } else if (!last_name_regex.test(last_name)){
                this.add_error("last_name", "W nazwisku można korzystać tylko z liter")
                return false;
            } else {
                this.clear_error("last_name")
                return true;
            }
        },
        validate_password(password, repeated_password){
             if ((password.replace(/\s/g, '')).length == 0){
                this.add_error("password", "Hasło jest wymagane do rejestracji")
                return false;
            } else if  ((password.replace(/\s/g, '')).length < 8) {
                this.add_error("password", "Minimalna ilość znaków to 8.")
                return false;
            } else if  ((password.replace(/\s/g, '')).length > 32) {
                this.add_error("password", "Maksymalna ilość znaków to 32.")
                return false;
            } else if (password != repeated_password){
                this.add_error("password", "Hasla nie zgadzają się")
                return false;
            } else {
                this.clear_error("password")
                return true;
            }
        },
        add_error(element_name, error_text){
            var form = document.getElementById(element_name);
            form.style.borderColor = "red"
            this.$root.$emit('bv::enable::tooltip', element_name + '_error')
            this.$root.$emit('bv::show::tooltip', element_name+ '_error')
            switch(element_name){
                case "email":
                    this.email_text = error_text
                    break
                case "first_name":
                    this.first_name_text = error_text
                    break
                case "last_name":
                    this.last_name_text = error_text
                    break
                case "password":
                   this.password_text = error_text
                   break
                }
        },
        clear_error(element_name){
            var form = document.getElementById(element_name);
            form.style.borderColor = "#ced4da"
            this.$root.$emit('bv::disable::tooltip', element_name + '_error')
        }
    }
}
</script>

<style scoped>
  .login-container{
    margin-top: 5%;
    margin-bottom: 5%;
}
.login-form{
    padding: 5%;
    box-shadow: 0 5px 8px 0 rgba(0, 0, 0, 0.2), 0 9px 26px 0 rgba(0, 0, 0, 0.19);
    margin-left:25%;
}
.login-form-1 h3{
    text-align: center;
    color: #333;
}
.login-container form{
    padding: 10%;
}
.btnSubmit
{
    width: 50%;
    border-radius: 1rem;
    padding: 1.5%;
    border: none;
    cursor: pointer;
}
.btnSubmit{
    font-weight: 600;
    color: #6998a3;
    background-color: #a4e6f4;
}
.btnSubmit:hover{
    color: #fff;
    background-color: #f3bac3;
}
.FormLinks{
    color: #6998a3;
    font-weight: 600;
    text-decoration: none;
}
</style>