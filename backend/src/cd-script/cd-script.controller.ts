import { Controller, Post, Body } from '@nestjs/common';
import { CDScriptService } from './cd-script.service';

@Controller('api/cd')
export class CDScriptController {
  constructor(private readonly cdScriptService: CDScriptService) {}

  @Post('create-release-note')
  async createReleaseNote(
    @Body()
    params: {
      projectId: string;
      lowerEnv: string;
      higherEnv: string;
      sourceBranch: string;
      destinationBranch: string;
    },
  ) {
    return this.cdScriptService.executeCreateReleaseNote(params);
  }

  @Post('generate-config')
  async generateConfig(
    @Body()
    params: {
      projectId: string;
      environment: string;
      releaseBranch: string;
    },
  ) {
    return this.cdScriptService.executeGenerateConfig(params);
  }

  @Post('deploy')
  async deploy(@Body() params: { projectId: string; type: string }) {
    return this.cdScriptService.executeDeploy(params);
  }
}
