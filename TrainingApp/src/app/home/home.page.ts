import { Component } from '@angular/core';
import { DataService, Data } from 'src/app/services/data.service';
declare var WifiWizard2: any;

@Component({
  selector: 'app-home',
  templateUrl: 'home.page.html',
  styleUrls: ['home.page.scss'],
})
export class HomePage {
  array_name: string[] = [];
  array_bssid: string[] = [];
  array_level: string[][] = [[]];
  clear_bssid: string[] = [];
  clear_level: string[][] = [[]];

  id = 0;
  count = 0;
  results = [];
  info_txt = '';

  idea: Data = {
    name: '',
    notes: '',
  };

  constructor(private dataService: DataService) {}
  ngOnInit() {}

  addIdea() {
    this.dataService.addIdea(this.idea).then(
      () => {
        console.log('Idea added');
      },
      (err) => {
        console.log('There was a problem adding your idea :(');
      }
    );
  }
  setDelay(i) {
    setTimeout(() => {
      console.log('i: ', i);
      this.count++;
      if (i == 3) {
        this.id++;
      }
      // this.getNetworks();
    }, 5000 * i);
  }

  click() {
    for (let i = 1; i <= 3; ++i) {
      this.setDelay(i);
    }
  }

  async getNetworks() {
    this.info_txt = 'loading...';
    try {
      let results = await WifiWizard2.scan();
      this.results = results;
      this.info_txt = '';
    } catch (error) {
      this.info_txt = error;
    }
  }

  filter(name: string, bssid: string, level: string) {
    this.array_name.push(name);
    this.array_bssid.push(bssid);
    this.array_level[this.id].push(level);
  }
  hi() {
    // this.array_name = this.clear;
  }
  hi2() {
    console.log(this.array_name);
  }
  hi3(name: string) {
    console.log('iddd: ', name);
    // this.array_name[0].push('trung');
  }
}
