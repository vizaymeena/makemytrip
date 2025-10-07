// states
import { useState } from 'react';

// css
import '../../assets/styles/searchforms/flightform.css'

// react-icons
import { LuLocate } from "react-icons/lu";
import { LiaExchangeAltSolid } from "react-icons/lia";

export default function FlightSearch() {

  let [selectedOption,setSelectedOption] = useState("oneway")


  // handle segment selection
  function handleSelect(option){
    setSelectedOption(option)
  }


  return (
    <div className="flight-search-container">

      <form className="flight-search-form">
        {/* trip segment */}
        <div className='segment-type'>

             <div className="div1">
        <div 
          className={`segment-option ${selectedOption === 'oneway' ? 'active' : ''}`}
          onClick={() => handleSelect('oneway')}
        >
          <input
            className="checkbox-input"
            type="radio"
            name="tripType"
            checked={selectedOption === 'oneway'}
            readOnly
          />
          <span className="segment-title">One Way</span>
        </div>

        <div 
          className={`segment-option ${selectedOption === 'roundtrip' ? 'active' : ''}`}
          onClick={() => handleSelect('roundtrip')}>
          <input
            className="checkbox-input"
            type="radio"
            name="tripType"
            checked={selectedOption === 'roundtrip'}
            readOnly
            />
          <span className="segment-title">Round Trip</span>
        </div>

        <div 
          className={`segment-option ${selectedOption === 'multicity' ? 'active' : ''}`}
          onClick={() => handleSelect('multicity')}
        >
          <input
            className="checkbox-input"
            type="radio"
            name="tripType"
            checked={selectedOption === 'multicity'}
            readOnly
          />
          <span className="segment-title">Multi City</span>
        </div>
      </div>
      </div>

        {/* form category */}
       <div className='fromToClass'>
        {/* From */}
        <div className="form-field">
          <label>From</label>
          <input className='field-from' type="text" placeholder="Enter origin city or airport" />
        </div>
        <div className='exchange-form'>
           <span className='exchnageicon'> <LiaExchangeAltSolid/></span>
        </div>
        {/* To */}
        <div className="form-field">
          <label>To</label>
          <input className='field-to' type="text" placeholder="Enter destination city or airport" />
        </div>

        {/* Departure */}
        <div className="form-field">
          <label>Departure</label>
          <input type="date" />
        </div>

        {/* Return */}
        <div className="form-field">
          <label>Return</label>
          <input type="date" />
        </div>

        {/* Travellers & Class */}
        <div className="form-field">
          <label>Travellers & Class</label>
          <select>
            <option>1 Traveller, Economy</option>
            <option>2 Travellers, Economy</option>
            <option>1 Traveller, Business</option>
            <option>2 Travellers, Business</option>
          </select>
        </div>
        
       </div>
   
        {/* special discount */}
        <div className="extra-savings">
          <h1>Extra Savings</h1>
          <div className="discount-options">

            <div className="discount-card">
              <div className='checkboxdiv'>
                <input type="radio"/> 
             </div> 
              <div>
                <h4>Regular</h4>
                <p>regular fares</p>
              </div>
            </div>

            <div className="discount-card">
                <div className='checkboxdiv'>
                <input type="radio"/> 
             </div> 
              <div>
                <h4>Student</h4>
                <p>extra discount/baggage</p>
              </div>
            </div>

            <div className="discount-card">
                <div className='checkboxdiv'>
                <input type="radio"/> 
             </div> 
              <div>
                <h4>Senior Citizen</h4>
                <p>upto Rs 600 off.</p>
              </div>
            </div>

            <div className="discount-card">
              <div className='checkboxdiv'>
                <input type="radio"/> 
               </div> 
              <div>
                <h4>Doctor & Nurses</h4>
                <p>upto Rs 600 off.</p>
              </div>
            </div>

            <div className="discount-card">
              <div className='checkboxdiv'>
                <input type="radio"/> 
              </div> 
              <div>
                <h4>Armed Forces</h4>
                <p>upto Rs 600 off.</p>
              </div>
            </div>
          </div>

          {/* Flight Tracker */}
          <div className="flight-tracker">
            <i> {<LuLocate/>}  </i>
            <span>Flight Tracker</span>
          </div>
        </div>

        {/* Search Button */}
        <div className="form-field search-btn-field">
          <button type="submit">Search</button>
        </div>
      </form>
    </div>
  );
}
