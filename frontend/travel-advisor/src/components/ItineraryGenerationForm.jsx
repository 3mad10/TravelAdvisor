import { React, useEffect, useState } from "react";
import { useForm, Controller } from "react-hook-form";
import DatePicker from 'react-datepicker';
import './Itinerary.css';
import api from "../api";
const ItineraryGenerationForm = ({responseCallback}) => {
  const {
        register,
        handleSubmit,
        control,
        formState: { errors },
  } = useForm();

  const [responseState, setResponseState] = useState(false);
  const [responseMessage, setResponseMessage] = useState('');
  const [responseInput, setResponseInput] = useState('');

  useEffect(() => {
    // console.log('entered effect of responseState');
    responseCallback(responseMessage, responseInput);
    setResponseState(false);
  }, [responseState]);

  const getResponse = async (formData) => {
    try {
      console.log("request : ")
      console.log(formData)
      const requestObject = {
        'destination':formData.destination,
        'interests':formData.interests.split(","),
        'start_date':formData.startDate.toISOString().split("T")[0],
        'end_date':formData.endDate.toISOString().split("T")[0],
      }
      const response = await api.post("/api/itinerary/generate", requestObject);
      setResponseState(true);
      setResponseMessage(response.data);
      setResponseInput(requestObject);
    }
    catch (error) {
      console.error("Error fetching generated plan", error);
    }
  }

  return (
    /* "handleSubmit" will validate your inputs before invoking "onSubmit" */
    <form onSubmit={handleSubmit(getResponse)}>
      <div>
        <input className="w-full text-xl focus:outline-none border-gray-300 px- border-4 rounded-2xl p-20 text-cyan-700 placeholder-cyan-700 focus:placeholder-cyan-600" placeholder="Where are you going?" {...register("destination", { required: true, maxLength: 256 })} />
        {errors.destination && <span className="text-sm">Please add your desination</span>}
      </div>
      <div>
        <input className="w-full text-sm focus:outline-none border-gray-300 px- border-4 rounded-2xl p-20 text-cyan-700 placeholder-cyan-700 focus:placeholder-cyan-600" placeholder="What are your interests? seperated by comma" {...register("interests", { pattern: /^[A-Za-z\s\,]+$/i })} />
        {errors.interests && <span className="text-sm">please add your interests with only characters spaces and commas between them</span>}
      </div>
      <div className="inline w-1/2 text-sm focus:outline-none border-gray-300 rounded-2xl p-20 text-cyan-700 focus:placeholder-cyan-600">
        <label>Start Date</label>
        <Controller
          control={control}
          name="startDate"
          defaultValue={new Date()}
          render={({ field }) => (
            <DatePicker
              showIcon
              selected={field.value}
              onChange={(date) => field.onChange(date)}
              icon={
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  width="1em"
                  height="1em"
                  viewBox="0 0 48 48"
                >
                  <mask id="ipSApplication0">
                    <g fill="none" stroke="#fff" strokeLinejoin="round" strokeWidth="4">
                      <path strokeLinecap="round" d="M40.04 22v20h-32V22"></path>
                      <path
                        fill="#fff"
                        d="M5.842 13.777C4.312 17.737 7.263 22 11.51 22c3.314 0 6.019-2.686 6.019-6a6 6 0 0 0 6 6h1.018a6 6 0 0 0 6-6c0 3.314 2.706 6 6.02 6c4.248 0 7.201-4.265 5.67-8.228L39.234 6H8.845l-3.003 7.777Z"
                      ></path>
                    </g>
                  </mask>
                  <path
                    fill="currentColor"
                    d="M0 0h48v48H0z"
                    mask="url(#ipSApplication0)"
                  ></path>
                </svg>
              }
            />
          )}
        />
        {errors.startDate && <span>{errors.startDate.message}</span>}
      </div>
      <div className="inline w-1/2 text-sm focus:outline-none border-gray-300 rounded-2xl p-20 text-cyan-700 focus:placeholder-cyan-600">
        <label>End Date</label>
        <Controller
          control={control}
          name="endDate"
          defaultValue={new Date()}
          render={({ field }) => (
            <DatePicker
              showIcon
              selected={field.value}
              onChange={(date) => field.onChange(date)}
              icon={
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  width="1em"
                  height="1em"
                  viewBox="0 0 48 48"
                >
                  <mask id="ipSApplication0">
                    <g fill="none" stroke="#fff" strokeLinejoin="round" strokeWidth="4">
                      <path strokeLinecap="round" d="M40.04 22v20h-32V22"></path>
                      <path
                        fill="#fff"
                        d="M5.842 13.777C4.312 17.737 7.263 22 11.51 22c3.314 0 6.019-2.686 6.019-6a6 6 0 0 0 6 6h1.018a6 6 0 0 0 6-6c0 3.314 2.706 6 6.02 6c4.248 0 7.201-4.265 5.67-8.228L39.234 6H8.845l-3.003 7.777Z"
                      ></path>
                    </g>
                  </mask>
                  <path
                    fill="currentColor"
                    d="M0 0h48v48H0z"
                    mask="url(#ipSApplication0)"
                  ></path>
                </svg>
              }
            />
          )}
        />
        {errors.endDate && <span>{errors.endDate.message}</span>}
      </div>
      <input className="w-xl rounded-2xl hover:bg-cyan-700 hover:text-white text-cyan-700 border-cyan-700 border-2 block ml-auto justify-center cursor-pointer" type="submit" value="Generate"/> 
    </form>
  )
}
export default ItineraryGenerationForm


