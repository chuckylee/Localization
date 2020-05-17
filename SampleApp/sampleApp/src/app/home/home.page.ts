import { Component, OnInit, ViewChild, ElementRef } from '@angular/core';
import { CaculatorSerivce } from '../service/caculator.service';

declare var WifiWizard2: any;

@Component({
  selector: 'app-home',
  templateUrl: 'home.page.html',
  styleUrls: ['home.page.scss'],
})
export class HomePage implements OnInit {
  results = [];
  infoTxt = '';
  arrayBssid: string[] = [];
  arrayLevel: number[][] = [[], [], [], [], [], [], [], [], [], []];
  RSSFinal: number[] = [];
  location: number[] = [];
  id = 0;
  countLevel = 0;
  check = true;
  // --------------------------------------------------------
  private ctx: CanvasRenderingContext2D;
  @ViewChild('canvas', { static: true })
  canvas: ElementRef<HTMLCanvasElement>;
  // --------------------------------------------------------
  constructor(private caculatorService: CaculatorSerivce) {}

  ngOnInit() {
    this.ctx = this.canvas.nativeElement.getContext('2d');
    this.ctx.fillStyle = 'red';
    this.ctx.fillRect(1 * 100 * 5, 0.7 * 100 * 5, 15, 15);
  }

  // hi() {
  //   const canvas = this.ctx.canvas;
  //   this.ctx.clearRect(0, 0, canvas.width, canvas.height);
  //   this.ctx.fillRect(this.x * 5, this.y * 5, 15, 15);
  //   this.x = this.x + 10;
  //   this.y = this.y + 10;
  // }

  setDelay(i) {
    setTimeout(() => {
      this.id++;
      this.getNetworks();
      // this.RSSFinal = this.caculatorService.caculatorRSS(
      //   this.arrayBssid,
      //   this.arrayLevel
      // );
      this.location = this.caculatorService.getLocation(
        this.arrayBssid,
        this.arrayLevel
      );
      this.print();
      this.getMap();
      this.caculatorService.clearData();
      if (i >= 11) {
        this.removeData();
      }
      console.log(i);
    }, 5000 * i);
  }

  click() {
    if (this.check) {
      for (let i = 1; i <= 500; ++i) {
        this.setDelay(i);
      }
    }
    this.check = false;
  }

  async getNetworks() {
    this.infoTxt = 'loading...';
    try {
      // tslint:disable-next-line:prefer-const
      let results = await WifiWizard2.scan();
      // tslint:disable-next-line:prefer-const
      for (let item of results) {
        if (
          !item.SSID.localeCompare('Le Duc Thanh') ||
          !item.SSID.localeCompare('DaiDuong1') ||
          !item.SSID.localeCompare('Nhat Quynh') ||
          !item.SSID.localeCompare('Tang tret')
        ) {
          // tslint:disable-next-line:prefer-const
          // tslint:disable-next-line:radix
          const level = parseInt(item.level);
          this.formatData(item.SSID, item.BSSID, level);
          this.results = results;
        }
      }
      this.results = results;
      this.infoTxt = '';
    } catch (error) {
      this.infoTxt = error;
    }
  }

  formatData(name: string, bssid: string, level: number) {
    if (this.id === 1) {
      this.arrayBssid.push(bssid);
      this.arrayLevel[this.countLevel].push(level);
      this.countLevel++;
    } else {
      // tslint:disable-next-line:prefer-const
      let bssidCurrent = this.arrayBssid.length;
      let check = true;
      for (let i = 0; i < bssidCurrent; i++) {
        if (!bssid.localeCompare(this.arrayBssid[i])) {
          this.arrayLevel[i].push(level);
          check = false;
          break;
        }
      }
      if (check === true) {
        // tslint:disable-next-line:prefer-const
        let k = this.arrayBssid.length;
        this.arrayBssid.push(bssid);
        this.arrayLevel[k - 1].push(level);
      }
    }
  }

  print() {
    console.log('----------------------');
    // tslint:disable-next-line:prefer-const
    let nameLenght = this.arrayBssid.length;
    for (let i = 0; i < nameLenght; i++) {
      console.log(
        'Real Data:  ',

        this.arrayBssid[i] + '  ' + '   [' + this.arrayLevel[i] + ']'
      );
    }
    console.log('RSSFinal: ', this.RSSFinal);
    console.log(
      'Location: [' + this.location[0] + ',' + this.location[1] + ']'
    );
    console.log('----------------------');
  }

  removeData() {
    for (let i = 0; i < this.arrayBssid.length; i++) {
      this.arrayLevel[i].shift();
    }
  }

  getMap() {
    const canvas = this.ctx.canvas;
    this.ctx.clearRect(0, 0, canvas.width, canvas.height);
    this.ctx.fillRect(
      this.location[0] * 100 * 5,
      this.location[1] * 100 * 5,
      15,
      15
    );
  }
}
