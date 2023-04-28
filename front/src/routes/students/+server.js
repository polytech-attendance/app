import fs from 'fs'

const rawStudentList = JSON.parse(fs.readFileSync('src/lib/students.json'),'utf-8');

function getByGroupId(groupId){
    
    let studentList = rawStudentList.Students.filter(student => student.group_id === groupId); 
    let groupResult = rawStudentList.Groups.filter(group => group.group_id === groupId);

    return {
      group: groupResult,
      students : studentList
    };
}

export function GET({url}){
    const groupId = Number(url.searchParams.get('groupId') ??  url.searchParams.get('groupId'));
    if (isNaN(groupId))
      throw error(400, 'invalid request');
    return new Response (JSON.stringify(getByGroupId(groupId)));
  };

