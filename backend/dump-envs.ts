import { PrismaClient } from '@prisma/client'
import * as fs from 'fs';

const prisma = new PrismaClient()

async function main() {
    const envs = await prisma.environment.findMany({ select: { name: true, projectId: true } });
    let output = "START_DUMP\n";
    envs.forEach(e => {
        output += `${e.name}|${e.projectId}\n`;
    });
    output += "END_DUMP";
    fs.writeFileSync('envs_dump.txt', output, 'utf8');
    console.log("Dump written to envs_dump.txt");
}

main()
    .catch((e) => {
        console.error(e)
        process.exit(1)
    })
    .finally(async () => {
        await prisma.$disconnect()
    })
