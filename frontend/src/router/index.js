import { createRouter, createWebHistory } from 'vue-router';
import MainPage from "../views/MainPage"
import AdminHome from "../views/AdminHome"
import AdminAdd from "../views/AdminAdd"
import AdminEdit from "../views/AdminEdit"
import AdminShow from "../views/AdminShow"
import ShowAdd from "../views/AddShow"
import EditShow from "../views/EditShow"
import AdminVenue from "../views/AdminVenue"
import VenueAdd from "../views/AddVenue"
import VenueEdit from "../views/EditVenue"
import UserHome from "../views/UserHome"
import Booking from "../views/Booking"
import AdminLogin from "../views/AdminLogin"
import UserHistory from "../views/UserHistory"
import UserSearch from "../views/UserSearch"
import AdminSummary from "../views/AdminSummary"
import UserLogin from "../views/UserLogin"
import UserSignUp from "../views/UserSignUp"
import VenueCSV from "../views/VenueCSV"
import jwt_decode from 'jwt-decode'

const routes = [
    {
        path:'/',
        name:'mainPage',
        component:MainPage,
        meta: { requiresAuth: false, requiresAdmin: false },
    },
    {
        path:"/admin/home/",
        name:'adminHome',
        component:AdminHome,
        meta: { requiresAuth: true, requiresAdmin: true },
    },
    {
        path:"/admin/add",
        name:"adminAdd",
        component:AdminAdd,
        meta: { requiresAuth: true, requiresAdmin: true },
    },
    {
        path:"/admin/edit/:id",
        name:"adminEdit",
        component:AdminEdit,
        props:true,
        meta: { requiresAuth: true, requiresAdmin: true },
    },
    {
        path:"/admin/shows",
        name: "adminShow",
        component:AdminShow,
        meta: { requiresAuth: true, requiresAdmin: true },
    },
    {
        path: "/admin/show_add",
        name: "showAdd",
        component: ShowAdd,
        meta: { requiresAuth: true, requiresAdmin: true },
    },
    {
        path: '/admin/show_edit/:id',
        name:'editShow',
        component: EditShow,
        props:true,
        meta: { requiresAuth: true, requiresAdmin: true },
        
    },
    {
        path: '/admin/venues',
        name: 'adminVenue',
        component: AdminVenue,
        meta: { requiresAuth: true, requiresAdmin: true },
    },
    {
        path: '/admin/venue_add',
        name: 'venueAdd',
        component: VenueAdd,
        meta: { requiresAuth: true, requiresAdmin: true },
    },
    {
        path: '/admin/venue_edit/:id',
        name:'editVenue',
        component: VenueEdit,
        props: true,
        meta: { requiresAuth: true, requiresAdmin: true },
    },
    {
        path: '/user/home',
        name: 'UserHome',
        component: UserHome,
        meta: { requiresAuth: true, requiresAdmin: false },
    },
    {
        path: '/user/booking/:id',
        name :'Booking',
        component: Booking,
        meta: { requiresAuth: true, requiresAdmin: false },
    },
    {
        path: '/admin/login',
        name:"adminLogin",
        component: AdminLogin,
        meta: { requiresAuth: false, requiresAdmin: false },
    },
    {
        path: '/user/bookings',
        name: "userHistory",
        component: UserHistory,
        meta: { requiresAuth: true, requiresAdmin: false },
    },
    {
        path: '/user/search',
        name: "userSearch",
        component: UserSearch,
        props: true,
        meta: { requiresAuth: true, requiresAdmin: false },
    },
    {
        path: "/admin/summary",
        name: "adminSummary",
        component: AdminSummary,
        meta: { requiresAuth: true, requiresAdmin: false },
    },
    {
        path: "/user/login",
        name: "userLogin",
        component: UserLogin,
        meta: { requiresAuth: false, requiresAdmin: false },
    },
    {
        path: "/user/signUp",
        name: "userSignUp",
        component: UserSignUp,
        meta: { requiresAuth: false, requiresAdmin: false },
    },
    {
        path: "/user/venue_details/:id",
        name: "venueCSV",
        component: VenueCSV,
        meta: { requiresAuth: true, requiresAdmin: true },
    },
]

const router = createRouter({
    mode: 'history',
    history: createWebHistory(),
    base: process.env.BASE_URL,
    routes,
  });

  function verifyToken(token) {
    try {
      const decoded = jwt_decode(token);
      return decoded;
    } catch (error) {
      console.error('Error verifying JWT:', error);
      return null;
    }
  }

  router.beforeEach((to, from, next) => {
    const isAuthenticated = localStorage.getItem('access_token');
    const isAdmin = localStorage.getItem('user_role') === 'admin';
  
    if (to.matched.some((record) => record.meta.requiresAuth)) {
      if (isAuthenticated == 'null') {
        alert("Please log in to continue.")
        next({ path: '/', query: { redirect: to.fullPath } });
      } else {
        try {
          const decodedToken = verifyToken(isAuthenticated)
          if (decodedToken && decodedToken.exp * 1000 > Date.now()) {
            if (to.matched.some((record) => record.meta.requiresAdmin) && !isAdmin) {
                alert("You are not an Admin, ACCESS DENIED!");
                next({ path: '/user/home', query: { redirect: to.fullPath } });
            } else {
              next();
            }
          } else {
            alert("Your Session has Expired")
            next({ path: '/', query: { redirect: to.fullPath } });
          }
        } catch (error) {
          console.error('Error decoding JWT:', error);
          next({ path: '/', query: { redirect: to.fullPath } });
        }
      }
    } else {
      next();
    }
  });
  
  
  export default router;