import React from 'react'
import '../../assets/styles/searchforms/cabform.css'

// react-icons
import { LiaExchangeAltSolid } from "react-icons/lia";

function CabSearch() {
  return (
    <>
    <form className='cab-form'>
        {/* flex item 1 */}
        <div className='cab-segment'>

            <div className='segment'>
                <input type="radio" />
                <span>Outstation One-Way</span>
            </div>

            <div className='segment'>
                <input type="radio" />
                <span>Outstation Round-Trip</span>
            </div>

             <div className='segment'>
                <input type="radio" />
                <span>Airport Transfer</span>
            </div>

             <div className='segment'>
                <input type="radio" />
                <span>Hourly Rentals</span>
            </div>
        </div>

        {/* flex item 2 */}
        <div className='cab-criteria'>
            <div className='from-to'>
                <div className='input-field'>
                    <span>From</span>
                    <input type="text" />
                </div>
                <span className='ex-icon'>
                    <LiaExchangeAltSolid/>
                </span>
                <div className='input-field'>
                    <span>To</span>
                    <input type="text" />
                </div>
            </div>
            <div className='cab-departure'>
                <span>Departure</span>
                <input type="date" />
                <span>wednesday</span>
            </div>
            <div className='cab-return'>
                <span>Return</span>
                <input type="date" />
                <span>wednesday</span>
            </div>

            <div className='cab-pickup-time'>
                <span>Pickup-Time</span>
                <input type="time" />

            </div>
          
        </div>

        <div className='cab-stops'>
            + Add Stops
        </div>

        <div className='btn-search'><button>Search</button></div>
    </form>
    </>
  )
}

export default CabSearch