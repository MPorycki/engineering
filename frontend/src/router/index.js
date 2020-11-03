import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from '../views/Home.vue'
import Login from '../views/Login.vue'
import Locations from '../views/Locations.vue'
import Registration from '../views/Registration.vue'
import PasswordResetVerification from '../views/PasswordResetVerification.vue'
import PasswordReset from '../views/PasswordReset.vue'
import VisitCreate from '../views/VisitCreate'
import AllVisits from '../views/AllVisits'
import VisitDetails from '../views/VisitDetails'
import VisitEdit from '../views/VisitEdit'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/about',
    name: 'About',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '../views/About.vue')
  },
  {
    path: '/login',
    name: 'Login',
    component: Login
  },
  {
    path: '/registration',
    name: 'Registration',
    component: Registration
  },
  {
    path: '/passresetverify',
    name: 'PasswordResetVerification',
    component: PasswordResetVerification
  },
  {
    path: '/passreset',
    name: 'PasswordReset',
    component: PasswordReset
  },
  {
    path: '/locations',
    name: 'Locations',
    component: Locations
  }
  ,
  {
    path: '/visitCreate',
    name: 'VisitCreate',
    component: VisitCreate
  },
  {
    path: '/visitsAll',
    name: 'AllVisits',
    component: AllVisits
  },
  {
    path: '/visitDetails',
    name: 'VisitDetails',
    component: VisitDetails
  },
  {
    path: '/visitEdit',
    name: 'VisitEdit',
    component: VisitEdit
  }
]

const router = new VueRouter({
  routes
})

export default router
