<template>
  <div class="home">
      <h1 id="welcome">Witamy na stronie naszych salonów</h1>
      <router-link to="/login" class="btnSubmit" >Logowanie</router-link>
  </div>
</template>

<script>
// @ is an alias to /src

export default {
  name: 'Home',
  components: {
    
  }
}
</script>

<style scoped>
body {
  height: 100%
}
  img {
    width: 100%;
    height: 100%;
  }
  .home {
    margin-bottom: -100px;
    width: 100%;
    min-height: 720px;
    background-image: url(../assets/hairdress1.jpeg);
    
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
  }

  #welcome{
    text-align: center;
    width: 100%;
    height: 100%;
  }
  .btnSubmit
  {
    width: 20%;
    border-radius: 1rem;
    padding: 1.5%;
    border: none;
    cursor: pointer;
  }
.btnSubmit{
    font-weight: 800;
    font-size: 25px;
    color: #6998a3;
    background-color: #a4e6f4;
  }
.btnSubmit:hover{
    color: #fff;
    background-color: #f3bac3;
  }
</style>