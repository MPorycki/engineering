<template>
    <div class="container login-container" >
            <div class="row">
                <div class="col-md-6 login-form">
                    <h3>Rejestracja</h3>
                    <form @submit.prevent="register">
                        <div class="form-group">
                            <input type="text" id="email" class="form-control" placeholder="Podaj swój email" value="" />
                            <b-tooltip target="email" id="email_error" class="rtooltips" triggers="hover" placement="right"  disabled="true" >{{email_text}}</b-tooltip>
                        </div>
                        <div class="form-group">
                            <input type="text" id="first_name" class="form-control" placeholder="Podaj swoje imię" value="" />
                            <b-tooltip target="first_name" id="first_name_error" class="rtooltips" triggers="hover" placement="right"  disabled="true">{{first_name_text}}</b-tooltip>
                        </div>
                        <div class="form-group">
                            <input type="text" id="last_name" class="form-control" placeholder="Podaj swoje nazwisko" value="" />
                            <b-tooltip target="last_name" id="last_name_error" class="rtooltips" triggers="hover" placement="right"  disabled="true">{{last_name_text}}</b-tooltip>
                        </div>
                        <div class="form-group">
                            <input type="password" id="password" class="form-control" placeholder="Wpisz hasło" value="" />
                            <b-tooltip target="password" id="password_error" class="rtooltips" triggers="hover" placement="right"  disabled="true">{{password_text}}</b-tooltip>
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
import backend_url from './variables'

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
                account_type: "customer"
            }
            this.add_error_text("first_name", "Dzialabanga");
            if (this.validate_form()){
                axios.post(backend_url + "account/", data).then(res => this.register_success(res.data)).catch(error => this.handle_error(error.response.data));
            }
        },
        register_success(message){
            alert(message);
            this.$router.push({ name: 'Login', })
        },
        handle_error(error_data){
            if (error_data["email_taken"]) {
                this.add_error_text("email_error", "Podany mail jest zajety");
            }
        },
        validate_form(){
            return false;
        },
        add_error_text(element_name, error_text){
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
.rtooltips{
    background-color:white;
    color:red;
    border-style: dotted
}
</style>