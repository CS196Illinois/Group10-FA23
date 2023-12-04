import React from 'react';
import {
  Switch,
  Text,
  View,
} from 'react-native';

import BackgroundGeolocation, {
  Location,
  Subscription
} from "react-native-background-geolocation";

const HelloWorld = () => {
  const [enabled, setEnabled] = React.useState(false);
  const [location, setLocation] = React.useState('');
  const [bikingDistance, setBikingDistance] = React.useState(0.0)

  React.useEffect(() => {
    /// 1.  Subscribe to events.
    const onLocation:Subscription = BackgroundGeolocation.onLocation((location) => {
      console.log('[onLocation]', JSON.stringify(location, null, 2));
      setLocation(JSON.stringify(location, null, 2));
      fetch('SERVER_URL_HERE', {
        method: 'POST',
        body: JSON.stringify(location, null, 2)
      }
      )
    })

    const onMotionChange:Subscription = BackgroundGeolocation.onMotionChange((event) => {
      console.log('[onMotionChange]', event);
    });

    const onActivityChange:Subscription = BackgroundGeolocation.onActivityChange((event) => {
      console.log('[onActivityChange]', event);
    })

    const onProviderChange:Subscription = BackgroundGeolocation.onProviderChange((event) => {
      console.log('[onProviderChange]', event);
    })

    /// 2. ready the plugin.
    BackgroundGeolocation.ready({
      // Geolocation Config
      desiredAccuracy: BackgroundGeolocation.DESIRED_ACCURACY_HIGH,
      distanceFilter: 1,
      // Activity Recognition
      stopTimeout: 100,
      // Application config
      debug: true, // <-- enable this hear sounds for background-geolocation life-cycle.
      logLevel: BackgroundGeolocation.LOG_LEVEL_VERBOSE,
      stopOnTerminate: false,   // <-- Allow the background-service to continue tracking when user closes the app.
      startOnBoot: true,        // <-- Auto start tracking when device is powered-up.
      // HTTP / SQLite config
      url: 'http://yourserver.com/locations',
      batchSync: false,       // <-- [Default: false] Set true to sync locations to server in a single HTTP request.
      autoSync: true,         // <-- [Default: true] Set true to sync each location to server as it arrives.
      headers: {              // <-- Optional HTTP headers
        "X-FOO": "bar"
      },
      params: {               // <-- Optional HTTP params
        "auth_token": "maybe_your_server_authenticates_via_token_YES?"
      }
    }).then((state) => {
      setEnabled(state.enabled)
      console.log("- BackgroundGeolocation is configured and ready: ", state.enabled);
    });

    return () => {
      // Remove BackgroundGeolocation event-subscribers when the View is removed or refreshed
      // during development live-reload.  Without this, event-listeners will accumulate with
      // each refresh during live-reload.
      onLocation.remove();
      onMotionChange.remove();
      onActivityChange.remove();
      onProviderChange.remove();
    }
  }, []);

  /// 3. start / stop BackgroundGeolocation
  React.useEffect(() => {
    if (enabled) {
      BackgroundGeolocation.start();
    } else {
      BackgroundGeolocation.stop();
      setLocation('');
    }
  }, [enabled]);

  setInterval(() => {
    let response = await fetch('http://127.0.0.1:5000/stat')
    console.log(response.json())
  }, 2000);

  return (
    <View style={{alignItems:'center'}}>
      <Text>Click to enable BackgroundGeolocation</Text>
      <Switch value={enabled} onValueChange={setEnabled} />
      <Text style={{fontFamily:'monospace', fontSize:12}}>{location}</Text>
      <Text>{bikingDistance}</Text>
    </View>
  )
}

// function Counter() {
//     useInterval(() => {
//       fetch('http://127.0.0.1:5000/stat').then(result => result.json()).then(result => result.stringify())
//     }, 1000);
//   }
//   import  { useState, useRef } from 'react';
//
//   function useInterval(callback, delay) {
//     const savedCallback = useRef();
//
//     // Remember the latest callback.
//     React.useEffect(() => {
//       savedCallback.current = callback;
//     }, [callback]);
//
//     // Set up the interval.
//     React.useEffect(() => {
//       function tick() {
//         savedCallback.current();
//       }
//       if (delay !== null) {
//         let id = setInterval(tick, delay);
//         return () => clearInterval(id);
//       }
//     }, [delay]);
//   }

export default HelloWorld;