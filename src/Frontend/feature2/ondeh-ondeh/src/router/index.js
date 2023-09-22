import { createRouter, createWebHistory } from "vue-router";
import BrowsingRoles from "../components/views/staff_browsing/RolesListingAll.vue"

const routes = [
    {
        path: '/browseroles',
        name: "Browsing Roles",
        component: BrowsingRoles
    }
]

const router = createRouter({
    history: createWebHistory(process.env.BASE_URL),
    routes
})

export default router