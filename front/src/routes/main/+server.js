import { json } from '@sveltejs/kit';
import fs from 'fs';

//the data should be crawled by BeautifulSoup on python. 

const scheduleData = JSON.parse(fs.readFileSync('src/lib/schedule.json', 'utf-8'));


//filter
function getByTeacherId(data, teacherID){
    //filter lessons where teacher is matched
    let daysFiltered = [];
    data.days.forEach(({weekday, date, lessons}) => {
      daysFiltered.push(
        {
          weekday: weekday,
          date: date,
          lessons: lessons.filter(lesson => {

            if (lesson.teachers === null) return false;

            return lesson.teachers.filter(teacher => {
              return (teacher.id === teacherID);
            }).length;
          })
        })
      });
    return {
      week: data.week,
      days: daysFiltered
    };
}



export function GET({url}) {
  const teacherId = Number(url.searchParams.get('teacherId') ??  url.searchParams.get('teacherId'));
  if (isNaN(teacherId))
    throw error(400, 'invalid request');
  const scheduleFiltered = getByTeacherId(scheduleData, teacherId);

  return new Response (JSON.stringify(scheduleFiltered));
};
