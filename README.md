##GTFS analysis package

***Query Example***
```javascript
db.vehicle_position.find({'timestamp': { $lte: new ISODate("2019-08-04T20:54:01Z")}})
```