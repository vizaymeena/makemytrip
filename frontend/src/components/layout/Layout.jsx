
import {Link,Outlet} from 'react-router-dom'
import '../../assets/styles/components-styles/layout.css'

// images
import indianFlag from '../../assets/images/flag.png'
import bgAtHome from '../../assets/images/background-at-home.jpeg'
import makemytrip from '../../assets/images/makemytrip.avif'
import flights from  '../../assets/images/flight.png'
import buses from  '../../assets/images/bus.png'
import hotels from  '../../assets/images/hotel.png'
import cabs from  '../../assets/images/cab.png'


// react-icons
import { FcBusinessman } from "react-icons/fc";
import { BsFillSuitcase2Fill } from "react-icons/bs";
import { FaUser } from "react-icons/fa";


// Search Form Component
import FlightSearch from '../search_forms/flightForm'
import HotelSearch from '../search_forms/Hotels'
import BusSearch from '../search_forms/Buses'
import CabSearch from '../search_forms/Cab'


// react state
import { useState } from 'react'



function Layout() {

  let [search,setSearch] = useState('flight') // search criteria form

  // function for selecting search option
  function handleSearch(e) {
      let option = e.target.closest(".search-option")
      if (!option) return

      let selectedSearch = option.dataset.service
      console.log(selectedSearch)
      setSearch(selectedSearch)

  }




  return (
    <>
    <div className='navbar-container'>
        <img className='background-home' src={bgAtHome} alt="" />

        {/* navbar */}
       <div className='nav-container-child1'>
         <div className='web-logo'>
            <img src={makemytrip} alt="" />

        </div>
        
        <div className='register-account'>
            <div className='register-bussiness'>
                <div className='nav-icon'>
                    <FcBusinessman/>
                </div>
                <div className='nav-info'>
                    <h4>Register business</h4>
                    <p>Grow your business</p>
                </div>
               
            </div>

            <div className='manage-booking'>
                <div className='nav-icon'>
                    <BsFillSuitcase2Fill/>
                </div>
                <div className='nav-info'>
                    <h4>My Trips</h4>
                    <p>Manage Your bookings</p>
                </div>
               
            </div>

            <div className='login-or-create-account'>
                <div className='nav-icon'>
                    <FaUser/>
                </div>
                <h4 className='nav-info'>Login or Create Account</h4>
                
            </div>

            <div className='select-lang-currency'>
                <span className='nav-icon'><img src={indianFlag} alt="country-flag" /></span>
                <span>INR</span> | 
                <span>English</span>
            </div>
        </div>
       </div>

       {/* Select Service Search Type */}

        <div className="search-options-container" onClick={handleSearch}>

          <div className="search-option" data-service="flight">
            <div className="icon-box">
              <img className="search-icon" src={flights} alt="Flights" />
            </div>
           <Link className='nav-link'>Flight</Link>
          </div>

          <div className="search-option" data-service="hotel">
            <div className="icon-box">
              <img className="search-icon" src={hotels} alt="Hotels" />
            </div>
            <Link className='nav-link' onClick={handleSearch} >Hotels</Link>
          </div>

          <div className="search-option" data-service="bus">
            <div className="icon-box">
              <img className="search-icon" src={buses} alt="Buses" />
            </div>
            <Link className='nav-link' onClick={handleSearch} >Buses</Link>
          </div>

          <div className="search-option" data-service="cab">
            <div className="icon-box">
              <img className="search-icon" src={cabs} alt="Cabs" />
            </div>
            <Link className='nav-link' onClick={handleSearch} >Cabs</Link>
          </div>

        </div>

        <div>

          {search == "flight" && <FlightSearch/>}
          {search == "hotel" && <HotelSearch/>}
          {search == "bus" && <BusSearch/>}
          {search == "cab" && <CabSearch/>}




        </div>

       



    </div>

   
    

    <Outlet/>

    <footer>

    </footer>
    </>
  )
}

export default Layout