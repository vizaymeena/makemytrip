import React from 'react'
import '../../assets/styles/searchforms/busform.css'

function BusSearch() {
  return (
    <div className='bus-search-container'>
    <form className='bus-form'>
      <div className='bus-ticket-form'>
        <div className='bus-origin'>
          <span>From</span>
          <input type="text" placeholder="Bhopal, Madhya Pradesh" />
          <span>India</span>
        </div>
        <div className='bus-destination'>
          <span>To</span>
          <input type="text" placeholder="Delhi, Delhi" />
          <span>India</span>
        </div>
        <div className='bus-travel-date'>
          <span>Travel Date</span>
          <input type="date" defaultValue="2025-10-01" />
          <span>Wednesday</span>
        </div>
      </div>
       <div className='btn-search'>
          <button>SEARCH</button>
        </div>
    </form>
    </div>
  )
}

export default BusSearch