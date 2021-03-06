import { Component, OnInit, ViewChild, ElementRef } from '@angular/core';
import { CaculatorSerivce } from '../service/caculator.service';
import { TrilaSerivce } from '../service/trilateration.service';
import { DataService, Data } from 'src/app/service/data.service';
import {
  AngularFirestore,
  AngularFirestoreCollection,
} from '@angular/fire/firestore';
import { Observable } from 'rxjs';
declare var WifiWizard2: any;
@Component({
  selector: 'app-home',
  templateUrl: 'home.page.html',
  styleUrls: ['home.page.scss'],
})
export class HomePage implements OnInit {
  ws: WebSocket;
  results = [];
  infoTxt = '';
  arrayName: string[] = [];
  arrayBssid: string[] = [];
  arrayLevel: number[][] = [[], [], [], [], [], [], [], [], [], []];
  RSSFinal: number[] = [];
  location: number[] = [];
  realLocation: number[] = [];
  accuracy = 0;
  id = 0;
  countLevel = 0;
  check = true;
  width = 14.4;
  height = 8.4;
  px = 37.795275591;
  x = 0.2;
  y = 0.2;
  database = [];
  setTimeOut = 1500;
  kNearest = 4;

  name: string[] = ['ESP32-5', 'ESP32-2', 'ESP32-3', 'ESP32-4', 'ESP32-1'];
  level: number[][] = [[-58], [-67], [-60], [-57], [-70]];
  // --------------------------------------------------------
  private locationCanvas: CanvasRenderingContext2D;
  private tableCanvas: CanvasRenderingContext2D;
  @ViewChild('canvas', { static: true })
  canvas: ElementRef<HTMLCanvasElement>;
  // --------------------------------------------------------
  postsCol: AngularFirestoreCollection<Data>;
  posts: Observable<Data[]>;
  newposts: Observable<Data[]>;
  // ---------------------------------------------------------
  constructor(
    private caculatorService: CaculatorSerivce,
    private trilaSerivce: TrilaSerivce, // private socket: Socket
    private afs: AngularFirestore
  ) { }

  ngOnInit() {
    this.locationCanvas = this.canvas.nativeElement.getContext('2d');
    this.tableCanvas = this.canvas.nativeElement.getContext('2d');
    this.initMap();
    // this.location = this.trilaSerivce.getLocation(this.name, this.level);

    this.postsCol = this.afs.collection('location');
    this.posts = this.postsCol.valueChanges();
    this.postsCol.snapshotChanges().subscribe((data) => {
      data.forEach((change) => {
        if (change.type === 'added') {
          console.log(change.payload.doc.id);
          console.log(change.payload.doc.data().x);
          console.log(change.payload.doc.data().y);
          if (change.payload.doc.data().x > 14.4 || change.payload.doc.data().x < 0 || change.payload.doc.data().y > 8.4 || change.payload.doc.data().y < 0) {
            this.getLocationCanvas(1, 1);
          } else {
            this.location[0] = change.payload.doc.data().x;
            this.location[1] = change.payload.doc.data().y;

            this.getLocationCanvas(
              change.payload.doc.data().x,
              change.payload.doc.data().y
            );
          }

        }
      });
    });
    // this.trilaSerivce.check(this.name, this.level);

    // this.locationCanvas.fillStyle = 'blue';
    // this.RP();
  }

  // RP() {
  //   for (let i = 1; i < 36; i = i + 3) {
  //     for (let j = 1; j < 21; j = j + 3) {
  //       this.locationCanvas.fillRect(
  //         (i * 0.4 * 1000) / this.width,
  //         (j * 0.4 * 600) / this.height,
  //         15,
  //         15
  //       );
  //     }
  //   }
  // }

  // setDelay(i) {
  //   setTimeout(() => {
  //     this.id++;
  //     this.getNetworks();
  //     // this.location = this.caculatorService.getLocation(
  //     //   this.arrayBssid,
  //     //   this.arrayLevel,
  //     //   this.kNearest
  //     // );
  //     // this.print();
  //     // this.getAccuracy();
  //     this.location = this.trilaSerivce.getLocation(
  //       this.arrayName,
  //       this.arrayLevel
  //     );
  //     this.print();
  //     this.getAccuracy();
  //     // this.getLocationCanvas();
  //     this.trilaSerivce.clearData();
  //     this.caculatorService.clearData();
  //     if (i >= 11) {
  //       this.removeData();
  //     }
  //     console.log(i);
  //   }, this.setTimeOut * i);
  // }

  // click() {
  //   if (this.check) {
  //     for (let i = 1; i <= 500; ++i) {
  //       this.setDelay(i);
  //     }
  //   }
  //   this.check = false;
  //   // console.log(this.caculatorService.database);
  // }
  // click() {
  //   this.location = this.trilaSerivce.getLocation(this.name, this.level);
  //   // this.getLocationCanvas();
  //   this.trilaSerivce.clearData();
  // }

  // async getNetworks() {
  //   this.infoTxt = 'loading...';
  //   try {
  //     let results = await WifiWizard2.scan();

  //     for (let item of results) {
  //       if (
  //         !item.SSID.localeCompare('UTS_709_IoT_1') ||
  //         !item.SSID.localeCompare('UTS_709_IoT_2') ||
  //         !item.SSID.localeCompare('EDISON-36') ||
  //         !item.SSID.localeCompare('EDISON-37') ||
  //         !item.SSID.localeCompare('ESP32-5') ||
  //         !item.SSID.localeCompare('ESP32-4') ||
  //         !item.SSID.localeCompare('ESP32-3') ||
  //         !item.SSID.localeCompare('ESP32-2') ||
  //         !item.SSID.localeCompare('ESP32-1')
  //       ) {
  //         // tslint:disable-next-line:radix
  //         const level = parseInt(item.level);
  //         this.formatData(item.SSID, item.BSSID, level);
  //         this.results = results;
  //       }
  //     }
  //     this.results = results;
  //     this.infoTxt = '';
  //   } catch (error) {
  //     this.infoTxt = error;
  //   }
  // }

  // formatData(name: string, bssid: string, level: number) {
  //   if (this.id === 1) {
  //     this.arrayName.push(name);
  //     this.arrayBssid.push(bssid);
  //     this.arrayLevel[this.countLevel].push(level);
  //     this.countLevel++;
  //   } else {
  //     let bssidCurrent = this.arrayBssid.length;
  //     let check = true;
  //     for (let i = 0; i < bssidCurrent; i++) {
  //       if (!bssid.localeCompare(this.arrayBssid[i])) {
  //         this.arrayLevel[i].push(level);
  //         check = false;
  //         break;
  //       }
  //     }
  //     if (check === true) {
  //       let k = this.arrayBssid.length;
  //       this.arrayName.push(name);
  //       this.arrayBssid.push(bssid);
  //       this.arrayLevel[k - 1].push(level);
  //     }
  //   }
  // }

  // print() {
  //   console.log('----------------------');

  //   let nameLenght = this.arrayBssid.length;
  //   for (let i = 0; i < nameLenght; i++) {
  //     console.log(
  //       'Real Data:  ',

  //       this.arrayName[i] + '  ' + '   [' + this.arrayLevel[i] + ']'
  //     );
  //   }
  //   console.log('RSSFinal: ', this.RSSFinal);
  //   console.log(
  //     'Location: [' + this.location[0] + ',' + this.location[1] + ']'
  //   );
  //   console.log('----------------------');
  // }

  // removeData() {
  //   for (let i = 0; i < this.arrayBssid.length; i++) {
  //     this.arrayLevel[i].shift();
  //   }
  // }

  getLocationCanvas(x: number, y: number) {
    const canvas = this.locationCanvas.canvas;
    this.locationCanvas.clearRect(0, 0, canvas.width, canvas.height);
    this.initMap();
    this.locationCanvas.fillStyle = 'blue';
    // this.locationCanvas.fillRect(
    //   (this.location[0] * 0.4 * 1000) / this.width,
    //   (this.location[1] * 0.4 * 600) / this.height,
    //   15,
    //   15
    // );
    this.locationCanvas.fillRect(
      (x * 1000) / this.width,
      (y * 600) / this.height,
      15,
      15
    );
  }

  initMap() {
    this.tableCanvas.fillStyle = 'black';
    this.tableCanvas.fillRect(
      (3.6 * 1000) / this.width,
      (0 * 600) / this.height,
      15,
      250
    );

    this.tableCanvas.fillStyle = 'black';
    this.tableCanvas.fillRect(
      (8 * 1000) / this.width,
      (0 * 600) / this.height,
      15,
      250
    );

    this.tableCanvas.fillStyle = 'black';
    this.tableCanvas.fillRect(
      (10.4 * 1000) / this.width,
      (0 * 600) / this.height,
      15,
      250
    );

    this.tableCanvas.fillStyle = 'black';
    this.tableCanvas.fillRect(
      (4.4 * 1000) / this.width,
      (5 * 600) / this.height,
      55.5,
      243
    );

    this.tableCanvas.fillStyle = 'black';
    this.tableCanvas.fillRect(
      (6 * 1000) / this.width,
      (5 * 600) / this.height,
      138.889,
      243
    );

    this.tableCanvas.fillStyle = 'black';
    this.tableCanvas.fillRect(
      (10 * 1000) / this.width,
      (5 * 600) / this.height,
      138.889,
      243
    );

    this.tableCanvas.fillStyle = 'black';
    this.tableCanvas.fillRect(
      (13.6 * 1000) / this.width,
      (0 * 600) / this.height,
      83.3,
      600
    );

    this.tableCanvas.fillStyle = 'black';
    this.tableCanvas.fillRect(
      (3.6 * 1000) / this.width,
      (3.3 * 600) / this.height,
      485,
      15
    );

    this.tableCanvas.fillStyle = 'silver';
    this.tableCanvas.fillRect(
      (0 * 1000) / this.width,
      (2 * 600) / this.height,
      139,
      114
    );

    this.tableCanvas.fillStyle = 'silver';
    this.tableCanvas.fillRect(
      (0 * 1000) / this.width,
      (6 * 600) / this.height,
      139,
      114
    );

    this.tableCanvas.fillStyle = 'silver';
    this.tableCanvas.fillRect(
      (4.4 * 1000) / this.width,
      (0.8 * 600) / this.height,
      200,
      114
    );

    this.tableCanvas.fillStyle = 'silver';
    this.tableCanvas.fillRect(
      (8.5 * 1000) / this.width,
      (0.8 * 600) / this.height,
      110,
      114
    );

    // this.tableCanvas.fillStyle = 'yellow';
    // this.tableCanvas.fillRect(
    //   (10.8 * 1000) / this.width,
    //   (0.4 * 600) / this.height,
    //   15,
    //   15
    // );

    // this.tableCanvas.fillStyle = 'yellow';
    // this.tableCanvas.fillRect(
    //   (14 * 1000) / this.width,
    //   (0.4 * 600) / this.height,
    //   15,
    //   15
    // );

    // this.tableCanvas.fillStyle = 'yellow';
    // this.tableCanvas.fillRect(
    //   (14 * 1000) / this.width,
    //   (8 * 600) / this.height,
    //   15,
    //   15
    // );

    // this.tableCanvas.fillStyle = 'yellow';
    // this.tableCanvas.fillRect(
    //   (10.8 * 1000) / this.width,
    //   (8 * 600) / this.height,
    //   15,
    //   15
    // );

    // this.tableCanvas.fillStyle = 'yellow';
    // this.tableCanvas.fillRect(
    //   (14 * 1000) / this.width,
    //   (4 * 600) / this.height,
    //   15,
    //   15
    // );
  }

  getRealLocation(e) {
    this.realLocation = [];
    let canvasElem = document.querySelector('canvas');
    let rect = canvasElem.getBoundingClientRect();
    let x = e.clientX - rect.left;
    let y = e.clientY - rect.top;
    console.log('Coordinate x: ' + x, 'Coordinate y: ' + y);
    this.realLocation.push((x * this.width) / 1000);
    this.realLocation.push((y * this.height) / 600);
    this.getAccuracy();
    console.log(
      'Real x: ' + this.realLocation[0],
      'Real y: ' + this.realLocation[1]
    );
  }

  getAccuracy() {
    this.accuracy = Math.sqrt(
      (this.realLocation[0] - this.location[0]) *
      (this.realLocation[0] - this.location[0]) +
      (this.realLocation[1] - this.location[1]) *
      (this.realLocation[1] - this.location[1])
    );
  }

  // getReferncePoint() {
  //   // setInterval(() => {
  //   this.database = this.caculatorService.getRPfromDatabase();
  //   console.log(this.database);

  //   // tslint:disable-next-line:prefer-for-of
  //   for (let i = 0; i < this.database.length; i++) {
  //     this.tableCanvas.save();
  //     this.tableCanvas.fillStyle = 'red';
  //     this.tableCanvas.fillRect(
  //       (parseFloat(this.database[i].location[0]) * 0.4 * 1000) / this.width,
  //       (parseFloat(this.database[i].location[1]) * 0.4 * 600) / this.height,
  //       15,
  //       15
  //     );
  //     this.tableCanvas.restore();
  //   }

  //   //   setTimeout(() => {
  //   //     this.clear();
  //   //   }, 10);
  //   // }, 20);
  // }

  clearCanvas() {
    const canvas = this.locationCanvas.canvas;
    this.locationCanvas.clearRect(0, 0, canvas.width, canvas.height);
  }
  // getKnearest() {}
}
