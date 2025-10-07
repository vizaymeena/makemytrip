import React from 'react'
import '../../assets/styles/searchforms/hotelform.css'

function HotelSearch() {
  return (
    <>
    <div className='hotelSearchContainer'>

        <form className='hotelSearchForm'>
            
           <div className='selectSegment'>
                 <div>
                    <input type="radio" />
                    <span>Upto 4 Rooms</span>
                </div>
                 <div>
                    <input type="radio" />
                    <span>Group Deals</span>
                </div>
           </div>
           <div className='hotelCriteria'>
                <div className='input-box-div'>
                    <span>City,Property Name or Location</span>
                    <input type="text" />
                    <span>City</span>
                </div>

                <div className='input-box-div'>
                    <span>Check-In</span>
                    <input type="date" />
                    <span>Monday</span>
                </div>

                <div className='input-box-div'>
                    <span>Check-Out</span>
                    <input type="date" />
                    <span>Monday</span>
                </div>

                <div className='input-box-div'>
                    <span>Room & Guest</span>
                    <input type="text" />
                </div>

                <div>
                    <span>price per night</span>
                    <select>
                        <option value={0-1500}>Rs upto 1500</option>
                        <option value={0-1500}>Rs 1500 - 2500</option><option value={0-1500}>Rs 2500 - 1500</option>
                        <option value={0-1500}>Rs 1500 - 2500</option><option value={0-1500}>Rs 5000+</option>
                    </select>
                </div>

           </div>

           <div className='btn-search-div'>
            <button>Search</button>
           </div>

        </form>

    </div>
    

    
    </>
  )
}

export default HotelSearch